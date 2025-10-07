import serial
import time

BIOPAC_EVENTS = {
    'S_plus' : 20,
    'S_0' : 21,
    'S_2' : 22,
    'S_4' : 23,
    'S_6' : 24,
    'S_8' : 25,
    'S_ITIpre': 26,
    'S_ITIpost':27,

    'N1_plus': 30,
    'N1_0': 31,
    'N1_2': 32,
    'N1_4': 33,
    'N1_6': 34,
    'N1_8': 35,
    'N1_ITIpre': 36,
    'N1_ITIpost':37,
    'N1_angry':38,

    'N2_plus': 40,
    'N2_0': 41,
    'N2_2': 42,
    'N2_4': 43,
    'N2_6': 44,
    'N2_8': 45,
    'N2_ITIpre': 46,
    'N2_ITIpost': 47,
    'N2_angry': 48,

    'N3_plus': 50,
    'N3_0': 51,
    'N3_2': 52,
    'N3_4': 53,
    'N3_6': 54,
    'N3_8': 55,
    'N3_ITIpre': 56,
    'N3_ITIpost':57,
    'N3_angry':58,

    'N4_plus': 60,
    'N4_0': 61,
    'N4_2': 62,
    'N4_4': 63,
    'N4_6': 64,
    'N4_8': 65,
    'N4_angry': 68,
    'N4_ITIpre': 66,
    'N4_ITIpost': 67,


    'N5_plus': 70,
    'N5_0': 71,
    'N5_2': 72,
    'N5_4': 73,
    'N5_6': 74,
    'N5_8': 75,
    'N5_ITIpre': 76,
    'N5_ITIpost': 77,
    'N5_angry': 78,

    'N6_plus': 80,
    'N6_0': 81,
    'N6_2': 82,
    'N6_4': 83,
    'N6_6': 84,
    'N6_8': 85,
    'N6_ITIpre': 86,
    'N6_ITIpost': 87,
    'N6_angry': 88,

    'N7_plus': 90,
    'N7_0': 91,
    'N7_2': 92,
    'N7_4': 93,
    'N7_6': 94,
    'N7_8': 95,
    'N7_ITIpre': 96,
    'N7_ITIpost': 97,
    'N7_angry': 98,

    'N8_plus': 100,
    'N8_0': 101,
    'N8_2': 102,
    'N8_4': 103,
    'N8_6': 104,
    'N8_8': 105,
    'N8_ITIpre': 106,
    'N8_ITIpost': 107,
    'N8_angry': 108,

    'PreVas_rating': 100,
    'PostVas_rating': 101,
    'preCond': 102,
    'cond': 103,
    'test': 104,
    'condNewVersion': 105,
    'testNewVersion': 106,
    'blankSlide': 107,
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