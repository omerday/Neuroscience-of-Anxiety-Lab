import time
import serial


"""
The method sends a signal according to the scenario given, to the serial port, then zero-s it back and closes the port.
List of scenarios:
    
    255 - Initialization

    Scenarios List indexing method:
    First digit (left):
        0 - N
        1 - P
        2 - U
    Second digit:
        1 - Condition Start
        2 - Cue Start
        3 - No-Cue Start
    Third digit:
        0 - No event
        1 - Startle
        2 - Shock
"""


def report_event(ser: serial.Serial, event_num: int):
    if not ser.is_open:
        ser.open()
    ser.write(hex(event_num).encode())
    time.sleep(0.05)
    ser.write("RR".encode())
    ser.close()