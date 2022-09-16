import serial
import time
#arduino = serial.Serial(port='/dev/cu.usbmodem11301', baudrate=57600, timeout=.1)
arduino = serial.Serial(port='/dev/ttyACM1', baudrate=57600, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(1)
    data = arduino.readline()
    return data
while True:
    num = input("Enter a number: ") # Taking input from user
    value = write_read(num)
    print(value) # printing the value