import time
import serial


"""
The method sends a signal according to the scenario given, to the serial port, then zero-s it back and closes the port.
List of scenarios:
    
    255 - Initialization
    80 - Startle Habituation
    99 - Calibration (Staring at the + for a minute)

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
        0 - Onset
        1 - Startle
        2 - Shock
"""


def report_event(ser: serial.Serial, event_num: int):
    if not ser.is_open:
        ser.open()
    print(f"Sending event {event_num} to BioPac - {hex(event_num).encode()}")
    ser.write(hex(event_num).encode())
    time.sleep(0.05)
    ser.write("RR".encode())
    ser.close()