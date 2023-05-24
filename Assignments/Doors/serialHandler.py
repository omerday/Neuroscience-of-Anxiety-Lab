import time
import serial


"""
The method sends a signal according to the scenario given, to the serial port, then zero-s it back and closes the port.
List of scenarios:
    
    255 - Initialization

    # Scenarios List indexing method:
    # (reward - 1) * 7 + Punishment - 1
    # For example:
    # Reward 1 Punishment 1 - index 0
    # Reward 5 Punishment 2 - index 29
    
    0-48 - Door start
    50-98 - Door lock
    100-148 - Door opening
"""


def report_event(ser: serial.Serial, event_num: int):
    if not ser.is_open:
        ser.open()
    ser.write(hex(event_num).encode())
    time.sleep(0.05)
    ser.write("RR".encode())
    ser.close()