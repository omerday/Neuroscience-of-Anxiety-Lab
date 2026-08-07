# Doors daily CSV export

Emails a CSV of each day's Doors task sessions to the lab, automatically.

Runs in GitHub Actions on a schedule — **nothing runs on a participant's phone**, and no
credentials are ever shipped in the app. The Doors app itself is untouched by this.

```
participants' phones  →  Firestore  →  GitHub Actions (daily 20:00)  →  CSV emailed
                          (already          reads, builds CSV,
                           happens)         sends mail
```

## Setup

### 1. Firebase service account key

The script needs read access to Firestore.

**Recommended — read-only.** If this key ever leaks, the worst case is someone reading data
rather than deleting it:

1. [Google Cloud Console → Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts),
   select the **doors-task-app** project
2. **Create service account**, name it `doors-csv-export`
3. Grant the role **Cloud Datastore Viewer** (Firestore read-only) → Done
4. Open the new account → **Keys** → **Add key** → **Create new key** → **JSON**

**Quicker but full-admin:** Firebase Console → ⚙️ Project settings → Service accounts →
Generate new private key. Works identically, but the key can also delete data.

### 2. Repository secrets

GitHub → repo **Settings** → **Secrets and variables** → **Actions** → **New repository secret**:

| Secret | Value |
|---|---|
| `FIREBASE_SERVICE_ACCOUNT` | the entire contents of the JSON key file |
| `SMTP_HOST` | `smtp.walla.co.il` |
| `SMTP_PORT` | `465` |
| `SMTP_USER` | `labreports@walla.co.il` |
| `SMTP_PASSWORD` | the mailbox password |
| `REPORT_EMAIL_TO` | recipient; comma-separate for several |

GitHub encrypts these and masks them in logs. Never commit them to the repo.

### 3. Test it

Actions tab → **Doors daily CSV report** → **Run workflow**. Tick **dry_run** for the first
attempt: it prints the CSV into the log and sends no mail. Untick it to send for real.

## Schedule

The daily window is **20:00 to 20:00, Israel time**. GitHub's scheduler only speaks UTC and
Israel shifts between UTC+2 and UTC+3, so the cron fires at 18:00 UTC — 21:00 local in summer,
20:00 in winter. The window boundary itself is anchored to 20:00 regardless, so a late run
never causes a gap or a duplicate.

A session finishing after 20:00 appears in the next day's report.

**On a day with no sessions, no email is sent.** This is deliberate, but it means a silent day
and a broken export look the same from the inbox. The Actions tab shows every run, and GitHub
emails you when a workflow fails.

## CSV format

Wide — one row per session, trials flattened into numbered columns:

```
sessionId, subjectId, userId, sessionStart, finalCoins, nTrials,
vas_pre_anxiety, vas_pre_anxiety_rt, vas_mid1_anxiety, ..., vas_post_happiness_rt,
trial1_reward, trial1_punish, trial1_distance, trial1_doorOpened, trial1_outcome,
trial1_didWin, trial1_rt, trial1_coinsAfter, trial1_ts,
trial2_reward, ...
```

Sessions in one file may have different trial counts; the header is sized to the longest and
shorter rows are padded, so the sheet stays rectangular. `VAS_MID` repeats once per block, so
mid-task columns are numbered (`vas_mid1_`, `vas_mid2_`); `pre` and `post` occur once and are not.

Written with a UTF-8 BOM so Excel opens it correctly, and text fields beginning with `=`, `+`,
`-` or `@` are prefixed with `'` so spreadsheets don't execute them. Numbers are exempt from
that, so negative values keep their minus sign.

## Backfilling

Actions tab → Run workflow → fill in **since** and **until** (`YYYY-MM-DD`, until is exclusive):

```
since: 2026-08-01
until: 2026-08-08
```

Sends one CSV covering that whole range.

## Running locally

```bash
cd Assignments/Doors/export
pip install -r requirements.txt
export FIREBASE_SERVICE_ACCOUNT="$(cat ~/Downloads/doors-task-app-....json)"
python daily_report.py --dry-run
python daily_report.py --since 2026-08-01 --until 2026-08-08 --dry-run
```

## Known data gaps

These come from how the app writes to Firestore, not from this script:

- **Post-task VAS answers are missing.** The app uploads to Firestore *before* the post-task
  VAS is shown, so `vas_responses` never contains the `VAS_POST` block. The `vas_post_*`
  columns will be empty. Fixing this is a small change in `DoorTaskViewModel`.
- **VAS response times are always 0.** The app hardcodes `responseTime = 0L` and never measures
  it, so every `vas_*_rt` column reads `0`.
- **`distanceMax` / `distanceMin` are always 0** in the app's records, so they aren't exported.

## When Firebase goes away

Only `fetch_sessions()` in `daily_report.py` knows where the data lives. Point it at the new
store and everything downstream — the CSV format, the schedule, the email, the secrets — carries
over unchanged.
