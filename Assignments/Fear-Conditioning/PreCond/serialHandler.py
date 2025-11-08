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

    'CS-_0': 30,
    'CS-_2': 31,
    'CS-_4': 32,
    'CS-_6': 33,
    'CS-_8': 34,
    'CS-_ITIstart': 35,
    'CS-_ITIend':36,
    'CS-_angry':37,

    'CS+_0': 40,
    'CS+_2': 41,
    'CS+_4': 42,
    'CS+_6': 43,
    'CS+_8': 44,
    'CS+_ITIstart': 45,
    'CS+_ITIend': 46,
    'CS+_angry': 47,

    'NEW_0': 50,
    'NEW_2': 51,
    'NEW_4': 52,
    'NEW_6': 53,
    'NEW_8': 54,
    'NEW_ITIstart': 55,
    'NEW_ITIend':56,
    'NEW_angry':57,

    'PreVas_rating': 240,
    'PostVas_rating': 241,
    'preCond': 242,
    'cond': 243,
    'test': 244,
    'condNewVersion': 245,
    'testNewVersion': 246,
    'blankSlide': 247,

    'square_0': 130,
    'square_2': 131,
    'square_4': 132,
    'square_6': 133,
    'square_8': 134,
    'square_ITIstart': 135,
    'square_ITIend': 136,

    'circle_0': 140,
    'circle_2': 141,
    'circle_4': 142,
    'circle_6': 143,
    'circle_8': 144,
    'circle_ITIstart': 145,
    'circle_ITIend': 146,

    'triangle_0': 150,
    'triangle_2': 151,
    'triangle_4': 152,
    'triangle_6': 153,
    'triangle_8': 154,
    'triangle_ITIstart': 155,
    'triangle_ITIend': 156,

    'rhombus_0': 160,
    'rhombus_2': 161,
    'rhombus_4': 162,
    'rhombus_6': 163,
    'rhombus_8': 164,
    'rhombus_ITIstart': 165,
    'rhombus_ITIend': 166,

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