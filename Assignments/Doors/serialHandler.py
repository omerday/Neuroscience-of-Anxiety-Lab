import time
import serial


"""
The method sends a signal according to the scenario given, to the serial port, then zero-s it back and closes the port.
List of scenarios:
    
    255 - Initialization

    # Scenarios List indexing method:
    # (reward - 1) * 7 + Punishment
    # For example:
    # Reward 1 Punishment 1 - index 1
    # Reward 5 Punishment 2 - index 30
    
    51-99 - Door start
    101-149 - Door lock
    151-199 - Door opening
"""


def report_event(ser: serial.Serial, event_num: int):
    if not ser.is_open:
        ser.open()
    print(f"Sending event {event_num} to BioPac - {hex(event_num).encode()}")
    ser.write(hex(event_num).encode())
    time.sleep(0.05)
    print(f"Sending event RR to BioPac - {'RR'.encode()}")
    ser.write("RR".encode())
    ser.close()