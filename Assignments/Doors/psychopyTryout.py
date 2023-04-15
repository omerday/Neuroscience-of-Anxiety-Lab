import time
import serial
import serial.tools.list_ports as list_ports

all_ports = list_ports.comports()
print(all_ports)

ser = serial.Serial('COM4', 115200, bytesize=serial.EIGHTBITS)

ser.write(bin(23))
