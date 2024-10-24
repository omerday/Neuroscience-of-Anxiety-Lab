import time
from datetime import datetime

EVENTS_ENCODING = {
    'fixation_run_start': 1,
    'emotional_slide_before_images': 10,
    'pic_base': 11,
    'block_rest': 15,
    'block_rating_neg': 16,
    'block_rating_pos': 17,
    'block_ITI': 18,
    'block_rating_neg_locked': 19,
    'block_rating_pos_locked': 20,
    'run_rest': 2,
    'run_rest_2': 4,
    'washout_task_ITI': 70,
    'washout_task_shape': 71,
    'washout_task_shape_dots': 72,
    'washout_task_shape2': 73,
    'washout_task_rate': 74,
    'washout_task_rate_locked': 75,

    'baseline_start': 200,
    'T1_start': 201,
    'DTI_fixation_start': 202,
    'DTI_video_start': 203,
}


"""
Events encoding documentation - as some of the usage of the events is block agnostic, it is clearer to elaborate here 
the value of each event:
Main task:
Fixation in the start of the run - 1
Rest between 3 blocks (before washout) - 2
Rest between 3 blocks (after washout) - 4
Slide shown before 4 negative images - 10
First negative image - 11 
Second negative image - 12
Third negative image - 13
Forth negative image - 14
Rest after 4 negative images - 15
Scale of negative emotions after 4 negative images - 16
Scale of positive emotions after 4 negative images - 17
ITI in negative block after scales - 18
User locked answer for negative emotional scale in negative block - 19
User locked answer for positive emotional scale in negative block - 20
Slide shown before 4 neutral images - 30
First neutral image - 31 
Second neutral image - 32
Third neutral image - 33
Forth neutral image - 34
Rest after 4 neutral images - 35
Scale of negative emotions after 4 neutral images - 36
Scale of positive emotions after 4 neutral images - 37
ITI in neutral block after scales - 38
User locked answer for negative emotional scale in neutral block - 39
User locked answer for positive emotional scale in neutral block - 40
Slide shown before 4 positive images - 50
First positive image - 51 
Second positive image - 52
Third positive image - 53
Forth positive image - 54
Rest after 4 positive images - 55
Scale of negative emotions after 4 positive images - 56
Scale of positive emotions after 4 positive images - 57
ITI in positive block after scales - 58
User locked answer for negative emotional scale in positive block - 59
User locked answer for positive emotional scale in positive block - 60
ITI in washout task - 70
Clean shape shown in washout task - 71
Shape with dots shown in washout task - 72
Clean shape shown again in washout task - 73
Scale for number of dots in washout task - 74
User locked answer for number of dots in washout task - 75

Other tasks:
baseline start - 200
T1 start - 201
DTI fixation start - 202
DTI video start - 203
"""


def report_event(ser, event_num, df_log, start_time, image_name=""):
    """
    Reports event event_num in 3 ways - print to console, writes to df_log, and sends to ser Serial object
    """
    print(f"{round(time.time(), 2)} - Sending event {event_num} to BioPac - {hex(event_num).encode()}")
    if df_log is not None:
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
