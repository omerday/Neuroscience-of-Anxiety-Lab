import serial
import time

BIOPAC_EVENTS = {
        'break': 16,

        'T2_ITIpre': 20,
        'T2_square1': 21,
        'T2_square2': 22,
        'T2_square3': 23,
        'T2_square4': 24,
        'T2_square5': 25,
        'T2_heat_pulse': 26,
        'T2_PainRatingScale': 27,
        'T2_ITIpost': 28,

        'T4_ITIpre': 40,
        'T4_square1': 41,
        'T4_square2': 42,
        'T4_square3': 43,
        'T4_square4': 44,
        'T4_square5': 45,
        'T4_heat_pulse': 46,
        'T4_PainRatingScale': 47,
        'T4_ITIpost': 48,

        'T6_ITIpre': 60,
        'T6_square1': 61,
        'T6_square2': 62,
        'T6_square3': 63,
        'T6_square4': 64,
        'T6_square5': 65,
        'T6_heat_pulse': 66,
        'T6_PainRatingScale': 67,
        'T6_ITIpost': 68,

        'T8_ITIpre': 80,
        'T8_square1': 81,
        'T8_square2': 82,
        'T8_square3': 83,
        'T8_square4': 84,
        'T8_square5': 85,
        'T8_heat_pulse': 86,
        'T8_PainRatingScale': 87,
        'T8_ITIpost': 88,

        'PreVas_rating': 90,
        'MidRun_rating': 91,
        'PostRun_rating': 92,

        'Fixation_cross': 95,

        'Start_Cycle': 100
    }

PARADIGM_2_BIOPAC_EVENTS = {
        'break': 16,

        'T2_ITIpre': 20,
        'T2_0': 21,
        'T2_2': 22,
        'T2_4': 23,
        'T2_6': 24,
        'T2_8': 25,
        'T2_heat_pulse': 26,
        'T2_PainRatingScale': 27,
        'T2_ITIpost': 28,

        'T4_ITIpre': 40,
        'T4_0': 41,
        'T4_2': 42,
        'T4_4': 43,
        'T4_6': 44,
        'T4_8': 45,
        'T4_heat_pulse': 46,
        'T4_PainRatingScale': 47,
        'T4_ITIpost': 48,

        'T6_ITIpre': 60,
        'T6_0': 61,
        'T6_2': 62,
        'T6_4': 63,
        'T6_6': 64,
        'T6_8': 65,
        'T6_heat_pulse': 66,
        'T6_PainRatingScale': 67,
        'T6_ITIpost': 68,

        'T8_ITIpre': 80,
        'T8_0': 81,
        'T8_2': 82,
        'T8_4': 83,
        'T8_6': 84,
        'T8_8': 85,
        'T8_heat_pulse': 86,
        'T8_PainRatingScale': 87,
        'T8_ITIpost': 88,

        'PreVas_rating': 90,
        'MidRun_rating': 91,
        'PostRun_rating': 92,

        'Fixation_cross': 95,

        'Start_Cycle': 100
    }


def report_event(ser: serial.Serial, event_num):
    print(f"{round(time.time(), 2)} - Sending event {event_num} to BioPac - {hex(event_num).encode()}")
    if not ser:
        return
    if not ser.is_open:
        ser.open()
    ser.write(hex(event_num).encode())
    time.sleep(0.05)
    # print(f"Sending event RR to BioPac - {'RR'.encode()}")
    ser.write("RR".encode())
    ser.close()