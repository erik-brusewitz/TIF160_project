
import serial
import time
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=57600, timeout=.1)
    
def check_for_return_value(value):
    for i in range(10):
        data = str(arduino.readline())
        data = data.replace("b", "")
        data = data.replace("'", "")
        print("value = " + str(value) + ", data = " + str(data))
        if data == value:
            return True
        time.sleep(0.2)
    
    return False

def same_package():
    while True:
        time.sleep(1)

        servo_id = 2
        new_pos = 1500
        data = str(servo_id) + str(new_pos)
        arduino.write(bytes(data, 'utf-8'))
        if check_for_return_value(data):
            print("Data sent and received successfully")
        else:
            print("Data sending failed")
            continue
            
        time.sleep(1)
        
def commandline_test():
    while True:
        data = input("Enter a number: ") # Taking input from user
        arduino.write(bytes(data, 'utf-8'))
        if check_for_return_value(data):
            print("Data sent and received successfully")
        else:
            print("Data sending failed")
            continue
            
        time.sleep(1)

commandline_test()
#same_package()