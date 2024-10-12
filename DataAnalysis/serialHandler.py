import time
from datetime import datetime

FIRST_RUN_EVENTS_ENCODING = {
    'fixation': 1,
    'emotional_slide': 10,
    'pic_base': 11,
    'block_rest': 15,
    'block_rating_neg': 16,
    'block_rating_pos': 17,
    'block_ITI': 18,
    'block_rating_locked': 19,
    'run_rest': 2,
    'run_rest_2': 4,
    'washout_task_ITI': 60,
    'washout_task_shape': 61,
    'washout_task_shape_dots': 62,
    'washout_task_shape2': 63,
    'washout_task_rate': 64,
}


SECOND_RUN_EVENTS_ENCODING = {
    'fixation': 101,
    'emotional_slide': 110,
    'pic_base': 111,
    'block_rest': 115,
    'block_rating_neg': 116,
    'block_rating_pos': 117,
    'block_ITI': 118,
    'block_rating_locked': 119,
    'run_rest': 102,
    'washout_task': 103,
    'run_rest_2': 104
}


def report_event(ser, event_num, df_log, start_time, image_name=""):
    print(f"{round(time.time(), 2)} - Sending event {event_num} to BioPac - {hex(event_num).encode()}")
    time_diff = (datetime.now() - start_time).total_seconds()
    df_log.loc[len(df_log)] = [time_diff, event_num, image_name]
    if not ser:
        return
    if not ser.is_open:
        ser.open()
    ser.write(hex(event_num).encode())
    time.sleep(0.05)
    ser.write("RR".encode())
    ser.close()
