import serial
import time

BIOPAC_EVENTS = {
    'S_plus' : 20,
    'S_0' : 21,
    'S_2' : 22,
    'S_4' : 23,
    'S_6' : 24,
    'S_8' : 25,
    'S_ITIstart': 26,
    'S_ITIend':27,

    'N1_plus': 30,
    'N1_0': 31,
    'N1_2': 32,
    'N1_4': 33,
    'N1_6': 34,
    'N1_8': 35,
    'N1_ITIstart': 36,
    'N1_ITIend':37,
    'N1_angry':38,

    'N2_plus': 40,
    'N2_0': 41,
    'N2_2': 42,
    'N2_4': 43,
    'N2_6': 44,
    'N2_8': 45,
    'N2_ITIstart': 46,
    'N2_ITIend': 47,
    'N2_angry': 48,

    'N3_plus': 50,
    'N3_0': 51,
    'N3_2': 52,
    'N3_4': 53,
    'N3_6': 54,
    'N3_8': 55,
    'N3_ITIstart': 56,
    'N3_ITIend':57,
    'N3_angry':58,

    'N4_plus': 60,
    'N4_0': 61,
    'N4_2': 62,
    'N4_4': 63,
    'N4_6': 64,
    'N4_8': 65,
    'N4_angry': 68,
    'N4_ITIstart': 66,
    'N4_ITIend': 67,


    'N5_plus': 70,
    'N5_0': 71,
    'N5_2': 72,
    'N5_4': 73,
    'N5_6': 74,
    'N5_8': 75,
    'N5_ITIstart': 76,
    'N5_ITIend': 77,
    'N5_angry': 78,

    'N6_plus': 80,
    'N6_0': 81,
    'N6_2': 82,
    'N6_4': 83,
    'N6_6': 84,
    'N6_8': 85,
    'N6_ITIstart': 86,
    'N6_ITIend': 87,
    'N6_angry': 88,

    'N7_plus': 90,
    'N7_0': 91,
    'N7_2': 92,
    'N7_4': 93,
    'N7_6': 94,
    'N7_8': 95,
    'N7_ITIstart': 96,
    'N7_ITIend': 97,
    'N7_angry': 98,

    'N8_plus': 100,
    'N8_0': 101,
    'N8_2': 102,
    'N8_4': 103,
    'N8_6': 104,
    'N8_8': 105,
    'N8_ITIstart': 106,
    'N8_ITIend': 107,
    'N8_angry': 108,

    'PreVas_rating': 110,
    'PostVas_rating': 111,
    'preCond': 112,
    'cond': 113,
    'test': 114,
    'condNewVersion': 115,
    'testNewVersion': 116,
    'blankSlide': 117,
}

BIOPAC_SHORT_EVENTS = {
    'S_plus' : 20,
    'S_0' : 21,
    'S_2' : 22,
    'S_4' : 23,
    'S_6' : 24,
    'S_8' : 25,
    'S_ITIstart': 26,
    'S_ITIend':27,

    'CS-_plus': 30,
    'CS-_0': 31,
    'CS-_2': 32,
    'CS-_4': 33,
    'CS-_6': 34,
    'CS-_8': 35,
    'CS-_ITIstart': 36,
    'CS-_ITIend':37,
    'CS-_angry':38,

    'CS+_plus': 40,
    'CS+_0': 41,
    'CS+_2': 42,
    'CS+_4': 43,
    'CS+_6': 44,
    'CS+_8': 45,
    'CS+_ITIstart': 46,
    'CS+_ITIend': 47,
    'CS+_angry': 48,

    'NEW_plus': 50,
    'NEW_0': 51,
    'NEW_2': 52,
    'NEW_4': 53,
    'NEW_6': 54,
    'NEW_8': 55,
    'NEW_ITIstart': 56,
    'NEW_ITIend':57,
    'NEW_angry':58,

    'PreVas_rating': 110,
    'PostVas_rating': 111,
    'preCond': 112,
    'cond': 113,
    'test': 114,
    'condNewVersion': 115,
    'testNewVersion': 116,
    'blankSlide': 117,
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