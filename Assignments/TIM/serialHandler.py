import serial
import time

EVENTS = {
        'break': hex(16),

        'T2_square1': hex(20),
        'T2_square2': hex(21),
        'T2_square3': hex(22),
        'T2_square4': hex(23),
        'T2_square5': hex(24),
        'T2_heat_pulse': hex(25),
        'T2_PainRatingScale': hex(26),

        'T4_square1': hex(40),
        'T4_square2': hex(41),
        'T4_square3': hex(42),
        'T4_square4': hex(43),
        'T4_square5': hex(44),
        'T4_heat_pulse': hex(45),
        'T4_PainRatingScale': hex(46),

        'T6_square1': hex(60),
        'T6_square2': hex(61),
        'T6_square3': hex(62),
        'T6_square4': hex(63),
        'T6_square5': hex(64),
        'T6_heat_pulse': hex(65),
        'T6_PainRatingScale': hex(66),

        'T8_square1': hex(80),
        'T8_square2': hex(81),
        'T8_square3': hex(82),
        'T8_square4': hex(83),
        'T8_square5': hex(84),
        'T8_heat_pulse': hex(85),
        'T8_PainRatingScale': hex(86),

        'PreVas_rating': hex(90),
        'MidRun_rating': hex(91),
        'PostRun_rating': hex(92),

        'Fixation_cross': hex(95),

        'Start_Cycle': hex(100)
    }


def report_event(ser: serial.Serial, event_num: int):
    if not ser.is_open:
        ser.open()
    print(f"Sending event {event_num} to BioPac - {hex(event_num).encode()}")
    ser.write(hex(event_num).encode())
    time.sleep(0.05)
    print(f"Sending event RR to BioPac - {'RR'.encode()}")
    ser.write("RR".encode())
    ser.close()