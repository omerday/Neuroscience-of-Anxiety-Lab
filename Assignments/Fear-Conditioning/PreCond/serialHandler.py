import serial
import time

BIOPAC_EVENTS = {
    'S_plus' : 0,
    'S_0' : 1,
    'S_2' : 2,
    'S_4' : 3,
    'S_6' : 4,
    'S_8' : 5,
    'S_ITIpre': 6,
    'S_ITIpost':7,

    'N1_plus': 10,
    'N1_0': 11,
    'N1_2': 12,
    'N1_4': 13,
    'N1_6': 14,
    'N1_8': 15,
    'N1_ITIpre': 16,
    'N1_ITIpost':17,
    'N1_angry':18,

    'N2_plus': 20,
    'N2_0': 21,
    'N2_2': 22,
    'N2_4': 23,
    'N2_6': 24,
    'N2_8': 25,
    'N2_ITIpre': 26,
    'N2_ITIpost':27,
    'N2_angry':28,

    'N3_plus': 30,
    'N3_0': 31,
    'N3_2': 32,
    'N3_4': 33,
    'N3_6': 34,
    'N3_8': 35,
    'N3_ITIpre': 36,
    'N3_ITIpost':37,
    'N3_angry':38,

    'N4_plus': 40,
    'N4_0': 41,
    'N4_2': 42,
    'N4_4': 43,
    'N4_6': 44,
    'N4_8': 45,
    'N4_angry': 48,
    'N4_ITIpre': 46,
    'N4_ITIpost': 47,


    'N5_plus': 50,
    'N5_0': 51,
    'N5_2': 52,
    'N5_4': 53,
    'N5_6': 54,
    'N5_8': 55,
    'N5_ITIpre': 56,
    'N5_ITIpost': 57,
    'N5_angry': 58,

    'N6_plus': 60,
    'N6_0': 61,
    'N6_2': 62,
    'N6_4': 63,
    'N6_6': 64,
    'N6_8': 65,
    'N6_ITIpre': 66,
    'N6_ITIpost': 67,
    'N6_angry': 68,

    'N7_plus': 70,
    'N7_0': 71,
    'N7_2': 72,
    'N7_4': 73,
    'N7_6': 74,
    'N7_8': 75,
    'N7_ITIpre': 76,
    'N7_ITIpost': 77,
    'N7_angry':78,

    'N8_plus': 80,
    'N8_0': 81,
    'N8_2': 82,
    'N8_4': 83,
    'N8_6': 84,
    'N8_8': 85,
    'N8_ITIpre': 86,
    'N8_ITIpost': 87,
    'N8_angry': 88,

    'PreVas_rating': 90,
    'PostVas_rating': 91,
    'preCond': 92,
    'cond': 93,
    'test': 94,
    'condNewVersion': 95,
    'testNewVersion': 96,
    'blankSlide': 97,
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