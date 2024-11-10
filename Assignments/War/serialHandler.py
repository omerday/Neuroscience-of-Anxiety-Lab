import time
from datetime import datetime

EVENTS_ENCODING = {
    'fixation_run_start': 21,
    'emotional_slide_before_images': 30,
    'pic_base': 31,
    'block_rest': 35,
    'block_rating_neg': 36,
    'block_rating_pos': 37,
    'block_ITI': 38,
    'block_rating_neg_locked': 39,
    'block_rating_pos_locked': 40,
    'run_rest': 22,
    'run_rest_2': 24,
    'washout_task_ITI': 90,
    'washout_task_shape': 91,
    'washout_task_shape_dots': 92,
    'washout_task_shape2': 93,
    'washout_task_rate': 94,
    'washout_task_rate_locked': 95,

    'baseline_start': 220,
    'T1_start': 221,
    'DTI_fixation_start': 222,
    'DTI_video_start': 223,
}


"""
Events encoding documentation - as some of the usage of the events is block agnostic, it is clearer to elaborate here 
the value of each event:
Main task:
Fixation in the start of the run - 21
Rest between 3 blocks (before washout) - 22
Rest between 3 blocks (after washout) - 24
Slide shown before 4 negative images - 30
First negative image - 31 
Second negative image - 32
Third negative image - 33
Forth negative image - 34
Rest after 4 negative images - 35
Scale of negative emotions after 4 negative images - 36
Scale of positive emotions after 4 negative images - 37
ITI in negative block after scales - 38
User locked answer for negative emotional scale in negative block - 39
User locked answer for positive emotional scale in negative block - 40
Slide shown before 4 neutral images - 50
First neutral image - 51 
Second neutral image - 52
Third neutral image - 53
Forth neutral image - 54
Rest after 4 neutral images - 55
Scale of negative emotions after 4 neutral images - 56
Scale of positive emotions after 4 neutral images - 57
ITI in neutral block after scales - 58
User locked answer for negative emotional scale in neutral block - 59
User locked answer for positive emotional scale in neutral block - 60
Slide shown before 4 positive images - 70
First positive image - 71 
Second positive image - 72
Third positive image - 73
Forth positive image - 74
Rest after 4 positive images - 75
Scale of negative emotions after 4 positive images - 76
Scale of positive emotions after 4 positive images - 77
ITI in positive block after scales - 78
User locked answer for negative emotional scale in positive block - 79
User locked answer for positive emotional scale in positive block - 80
ITI in washout task - 90
Clean shape shown in washout task - 91
Shape with dots shown in washout task - 92
Clean shape shown again in washout task - 93
Scale for number of dots in washout task - 94
User locked answer for number of dots in washout task - 95

Other tasks:
baseline start - 220
T1 start - 221
DTI fixation start - 222
DTI video start - 223
"""


def report_event(ser, event_num, df_log, start_time, image_name="", duration=None):
    """
    Reports event event_num in 3 ways - print to console, writes to df_log, and sends to ser Serial object
    """
    print(f"{round(time.time(), 2)} - Sending event {event_num} to BioPac - {hex(event_num).encode()}")
    if df_log is not None:
        time_diff = (datetime.now() - start_time).total_seconds()
        df_log.loc[len(df_log)] = [time_diff, event_num, image_name, duration]
    if not ser:
        return
    if not ser.is_open:
        ser.open()
    ser.write(hex(event_num).encode())
    time.sleep(0.05)
    ser.write("RR".encode())
    ser.close()
