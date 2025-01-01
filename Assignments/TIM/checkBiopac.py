import serialHandler
import serial
import time

ser = serial.Serial('COM4', 115200, bytesize=serial.EIGHTBITS, timeout=1)
for i in range(20):
    serialHandler.report_event(ser, 250)

time.sleep(.5)

print(f"{round(time.time(), 2)} - Sending event {251} (long) to BioPac - {hex(251).encode()}")
if not ser.is_open:
    ser.open()
ser.write(hex(251).encode())
time.sleep(1)
# print(f"Sending event RR to BioPac - {'RR'.encode()}")
ser.write("RR".encode())
ser.close()

time.sleep(.5)

ser = serial.Serial('COM4', 115200, bytesize=serial.EIGHTBITS, timeout=1)
for i in range(20):
    serialHandler.report_event(ser, 250)