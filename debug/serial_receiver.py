import serial
import time
arduino = serial.Serial(port='/dev/ttyACM1', baudrate=57600, timeout=.1)

while True:
    time.sleep(0.05)
    data = arduino.readline()
    print(data)