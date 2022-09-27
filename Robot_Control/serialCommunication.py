import serial
import time

#arduino = serial.Serial(port='/dev/ttyACM0', baudrate=57600, timeout=.1)
arduino = serial.Serial(port='/dev/cu.usbmodem11301', baudrate=57600, timeout=.1)

def check_for_return_value(value):
    for i in range(40):
        data = str(arduino.readline())
        data = data.replace("b", "")
        data = data.replace("'", "")
        print("value = " + str(value) + ", data = " + str(data))
        if data == value:
            return True
        time.sleep(0.2)
    
    return False

def send_package(data):
    arduino.write(bytes(data, 'utf-8'))
    if check_for_return_value(data):
        print("Data sent and received successfully")
        return True
    else:
        print("Data sending failed")
        return False

def initialize_communication():
    for i in range(10):
        print("Establishing serial communication...")
        if (send_package("99999")):
            print("Serial communication established")
            return True
    print("Serial communication failed")
    return False