#!/usr/bin/env python3
"""
Daily CSV export for the Doors task.

Reads completed sessions from Firestore, renders them as one wide CSV (one row per session,
trials flattened into numbered columns), and emails it.

Runs on a schedule in GitHub Actions - see .github/workflows/doors-daily-report.yml. Nothing
about this runs on a participant's phone, so no credentials are ever distributed.

Deliberately structured so that only `fetch_sessions` knows about Firestore. When the lab
migrates off Firebase, that one function is rewritten and everything below it is untouched.

Local usage:
    export FIREBASE_SERVICE_ACCOUNT="$(cat service-account.json)"
    python daily_report.py --dry-run                  # print CSV, send nothing
    python daily_report.py --since 2026-08-01 --until 2026-08-08 --dry-run
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import smtplib
import ssl
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from email.message import EmailMessage
from typing import Any, Iterable
from zoneinfo import ZoneInfo

LAB_TZ = ZoneInfo("Asia/Jerusalem")
COLLECTION = "completed_sessions"

# Order trial columns are emitted in, per trial.
TRIAL_FIELDS = [
    "reward", "punish", "distance", "doorOpened",
    "outcome", "didWin", "rt", "coinsAfter", "ts",
]

META_COLUMNS = [
    "sessionId", "subjectId", "userId", "sessionStart",
    "finalCoins", "nTrials",
]

PHASE_RANK = {"VAS_PRE": 0, "VAS_MID": 1, "VAS_POST": 2}


# --------------------------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------------------------

@dataclass
class Trial:
    reward: int | None = None
    punish: int | None = None
    distance: float | None = None
    door_opened: bool | None = None
    outcome: str | None = None
    did_win: bool | None = None
    rt: float | None = None
    coins_after: int | None = None
    ts: int | None = None


@dataclass
class Vas:
    phase: str = ""
    tag: str = ""
    score: int | None = None
    rt: int | None = None
    ts: int | None = None


@dataclass
class Session:
    session_id: str
    subject_id: str
    user_id: str
    started_at_ms: int | None
    final_coins: int | None
    trials: list[Trial] = field(default_factory=list)
    vas: list[Vas] = field(default_factory=list)


# --------------------------------------------------------------------------------------------
# Firestore - the ONLY part that knows where the data lives
# --------------------------------------------------------------------------------------------

def fetch_sessions(since: datetime, until: datetime) -> list[Session]:
    """Sessions whose sessionTimestamp falls in [since, until)."""
    from google.cloud import firestore
    from google.cloud.firestore_v1.base_query import FieldFilter
    from google.oauth2 import service_account

    raw = os.environ.get("FIREBASE_SERVICE_ACCOUNT", "").strip()
    if not raw:
        sys.exit("FIREBASE_SERVICE_ACCOUNT is not set. See Assignments/Doors/export/README.md")

    try:
        info = json.loads(raw)
    except json.JSONDecodeError as exc:
        sys.exit(f"FIREBASE_SERVICE_ACCOUNT is not valid JSON: {exc}")

    credentials = service_account.Credentials.from_service_account_info(info)
    client = firestore.Client(project=info["project_id"], credentials=credentials)

    since_ms = int(since.timestamp() * 1000)
    until_ms = int(until.timestamp() * 1000)

    # FieldFilter rather than the positional where(field, op, value) form, which is deprecated
    # and would break on a future google-cloud-firestore release.
    query = (
        client.collection(COLLECTION)
        .where(filter=FieldFilter("sessionTimestamp", ">=", since_ms))
        .where(filter=FieldFilter("sessionTimestamp", "<", until_ms))
    )
    return [parse_session(doc.id, doc.to_dict() or {}) for doc in query.stream()]


def parse_session(doc_id: str, doc: dict[str, Any]) -> Session:
    session = Session(
        session_id=doc_id,
        subject_id=str(doc.get("subjectId") or ""),
        user_id=str(doc.get("userId") or ""),
        started_at_ms=as_int(doc.get("sessionTimestamp")),
        final_coins=as_int(doc.get("finalCoinTotal")),
    )

    # behavioral_data is written by the app in trial order; sort defensively on subtrial in
    # case Firestore ever hands the array back differently.
    behavioral = doc.get("behavioral_data") or []
    for entry in sorted(behavioral, key=lambda e: as_int(e.get("subtrial")) or 0):
        session.trials.append(Trial(
            reward=as_int(entry.get("rewardMagnitude")),
            punish=as_int(entry.get("punishmentMagnitude")),
            distance=as_float(entry.get("distanceFromDoor")),
            door_opened=entry.get("doorOpened"),
            outcome=entry.get("doorOutcome"),
            did_win=entry.get("didWin"),
            rt=as_float(entry.get("doorActionRT")),
            coins_after=as_int(entry.get("totalCoins")),
            ts=as_int(entry.get("timestamp")),
        ))

    for entry in doc.get("vas_responses") or []:
        session.vas.append(Vas(
            phase=str(entry.get("taskPhase") or ""),
            tag=str(entry.get("tag") or ""),
            score=as_int(entry.get("score")),
            rt=as_int(entry.get("responseTime")),
            ts=as_int(entry.get("timestamp")),
        ))

    return session


def as_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def as_float(value: Any) -> float | None:
    try:
        return round(float(value), 2)
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------------------------------------
# Wide CSV
# --------------------------------------------------------------------------------------------

def vas_key(entry: Vas, occurrence: int) -> tuple[str, str, int]:
    return (entry.phase, entry.tag, occurrence)


def index_vas(session: Session) -> dict[tuple[str, str, int], Vas]:
    """Number repeated (phase, tag) pairs - VAS_MID recurs once per block."""
    seen: dict[tuple[str, str], int] = {}
    indexed = {}
    for entry in session.vas:
        pair = (entry.phase, entry.tag)
        seen[pair] = seen.get(pair, 0) + 1
        indexed[vas_key(entry, seen[pair])] = entry
    return indexed


def vas_columns(sessions: Iterable[Session]) -> list[tuple[tuple[str, str, int], str]]:
    """Ordered (key, column_name) pairs covering every VAS answer across all sessions."""
    keys: list[tuple[str, str, int]] = []
    tag_order: list[str] = []
    for session in sessions:
        for key in index_vas(session):
            if key not in keys:
                keys.append(key)
        for entry in session.vas:
            if entry.tag not in tag_order:
                tag_order.append(entry.tag)

    max_occurrence: dict[str, int] = {}
    for phase, _tag, occurrence in keys:
        max_occurrence[phase] = max(max_occurrence.get(phase, 1), occurrence)

    def sort_key(key):
        phase, tag, occurrence = key
        return (
            PHASE_RANK.get(phase, 99), phase, occurrence,
            tag_order.index(tag) if tag in tag_order else 99,
        )

    columns = []
    for key in sorted(keys, key=sort_key):
        phase, tag, occurrence = key
        short = phase.replace("VAS_", "").lower() or "unknown"
        suffix = str(occurrence) if max_occurrence.get(phase, 1) > 1 else ""
        columns.append((key, f"vas_{short}{suffix}_{tag.lower()}"))
    return columns


def guard_formula(value: str) -> str:
    """Stop spreadsheets executing text fields. Only ever applied to strings, so negative
    numbers keep their leading minus sign."""
    if value and value[0] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + value
    return value


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return value
    return guard_formula(str(value))


def build_csv(sessions: list[Session]) -> str:
    if not sessions:
        return ""

    sessions = sorted(sessions, key=lambda s: s.started_at_ms or 0)
    columns = vas_columns(sessions)
    max_trials = max(len(s.trials) for s in sessions)

    header = list(META_COLUMNS)
    for _key, name in columns:
        header += [name, f"{name}_rt"]
    for i in range(1, max_trials + 1):
        header += [f"trial{i}_{field_name}" for field_name in TRIAL_FIELDS]

    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\r\n")
    writer.writerow(header)

    for session in sessions:
        row: list[Any] = [
            cell(session.session_id),
            cell(session.subject_id),
            cell(session.user_id),
            cell(format_time(session.started_at_ms)),
            cell(session.final_coins),
            cell(len(session.trials)),
        ]

        indexed = index_vas(session)
        for key, _name in columns:
            answer = indexed.get(key)
            row += [cell(answer.score if answer else None), cell(answer.rt if answer else None)]

        for i in range(max_trials):
            trial = session.trials[i] if i < len(session.trials) else None
            if trial is None:
                row += [""] * len(TRIAL_FIELDS)
            else:
                row += [
                    cell(trial.reward), cell(trial.punish), cell(trial.distance),
                    cell(trial.door_opened), cell(trial.outcome), cell(trial.did_win),
                    cell(trial.rt), cell(trial.coins_after), cell(trial.ts),
                ]

        writer.writerow(row)

    return buffer.getvalue()


def format_time(millis: int | None) -> str:
    """Space-separated rather than ISO 8601 'T' - Excel parses this straight to a datetime."""
    if not millis:
        return ""
    return datetime.fromtimestamp(millis / 1000, LAB_TZ).strftime("%Y-%m-%d %H:%M:%S")


# --------------------------------------------------------------------------------------------
# Email
# --------------------------------------------------------------------------------------------

def send_email(subject: str, body: str, filename: str, csv_text: str) -> None:
    host = require_env("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT", "465"))
    user = require_env("SMTP_USER")
    password = require_env("SMTP_PASSWORD")
    recipients = [a.strip() for a in require_env("REPORT_EMAIL_TO").split(",") if a.strip()]

    message = EmailMessage()
    message["From"] = os.environ.get("REPORT_EMAIL_FROM", "").strip() or user
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.set_content(body)

    # utf-8-sig writes a BOM so Excel opens the file as UTF-8 instead of the local codepage.
    message.add_attachment(
        csv_text.encode("utf-8-sig"),
        maintype="text", subtype="csv", filename=filename,
    )

    context = ssl.create_default_context()

    def attempt() -> None:
        if port == 465:
            with smtplib.SMTP_SSL(host, port, context=context, timeout=60) as server:
                server.login(user, password)
                server.send_message(message)
        else:
            with smtplib.SMTP(host, port, timeout=60) as server:
                server.starttls(context=context)
                server.login(user, password)
                server.send_message(message)

    # A failed run does NOT get retried by tomorrow's run - tomorrow covers tomorrow's window,
    # so a day lost here needs a manual backfill. Worth a few retries on transient network or
    # greylisting failures before giving up.
    last_error: Exception | None = None
    for delay in (0, 30, 120):
        if delay:
            print(f"Send failed, retrying in {delay}s...")
            time.sleep(delay)
        try:
            attempt()
            return
        except smtplib.SMTPAuthenticationError:
            raise  # Bad credentials will never succeed on retry.
        except (smtplib.SMTPException, OSError) as exc:
            last_error = exc

    raise RuntimeError(f"Could not send after 3 attempts: {last_error}")


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        sys.exit(f"{name} is not set. See Assignments/Doors/export/README.md")
    return value


# --------------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------------

def resolve_window(args) -> tuple[datetime, datetime]:
    """
    The 24 hours ending at the most recent send time.

    Anchored to a fixed hour rather than measured back from 'now', so that GitHub's scheduler
    running a few minutes late doesn't leave a gap or double-send.
    """
    if args.since or args.until:
        if not (args.since and args.until):
            sys.exit("--since and --until must be given together")
        since = datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=LAB_TZ)
        until = datetime.strptime(args.until, "%Y-%m-%d").replace(tzinfo=LAB_TZ)
        return since, until

    hour = int(os.environ.get("REPORT_HOUR", "20"))
    now = datetime.now(LAB_TZ)
    until = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    if until > now:
        until -= timedelta(days=1)
    return until - timedelta(days=1), until


def main() -> int:
    parser = argparse.ArgumentParser(description="Email a daily CSV of Doors task sessions.")
    parser.add_argument("--since", help="Start date YYYY-MM-DD (inclusive), for manual backfill")
    parser.add_argument("--until", help="End date YYYY-MM-DD (exclusive), for manual backfill")
    parser.add_argument("--dry-run", action="store_true", help="Print the CSV instead of emailing")
    args = parser.parse_args()

    since, until = resolve_window(args)
    print(f"Window: {since:%Y-%m-%d %H:%M} to {until:%Y-%m-%d %H:%M} ({LAB_TZ})")

    sessions = fetch_sessions(since, until)
    print(f"Found {len(sessions)} session(s)")

    if not sessions:
        # Silent on empty days, by choice - no heartbeat email.
        print("Nothing to send.")
        return 0

    csv_text = build_csv(sessions)

    if args.dry_run:
        print("--- CSV ---")
        print(csv_text)
        return 0

    label = f"{until:%Y-%m-%d}"
    plural = "" if len(sessions) == 1 else "s"
    send_email(
        subject=f"Doors Task data - {label} ({len(sessions)} session{plural})",
        body=(
            f"Automated export from the Doors task.\n\n"
            f"Window : {since:%Y-%m-%d %H:%M} to {until:%Y-%m-%d %H:%M} ({LAB_TZ})\n"
            f"Sessions: {len(sessions)}\n\n"
            f"One row per session. Trial columns are numbered "
            f"(trial1_reward, trial1_distance, ...).\n"
        ),
        filename=f"doors_{label}.csv",
        csv_text=csv_text,
    )
    print(f"Emailed {len(sessions)} session(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
