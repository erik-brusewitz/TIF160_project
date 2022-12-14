import serial
import time
import cv2

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
        

def check_for_return_value(cap, arduino, value, verbose, debug):
    animation = "|/-\\"
    
    for i in range(100):

        ret, frame = cap.read()
        cv2.imshow('shapes', frame)
        cv2.waitKey(1)

        print(animation[i % len(animation)], end="\r")

        data = str(arduino.readline())
        data = data.replace("b", "")
        data = data.replace("'", "")
        if debug:
            print("value = " + str(value) + ", data = " + str(data))
        if data == value:
            return True
        #time.sleep(0.2)
    
    return False

def send_package(cap, arduino, data, verbose, debug):
    if verbose:
        print("Sending " + data)
    arduino.write(bytes(data, 'utf-8'))
    if check_for_return_value(cap, arduino, data, verbose, debug):
        if verbose:
            print("Data sent and received successfully")
        return True
    else:
        if verbose:
            print("Data sending failed")
        return False

def initialize_communication(cap, arduino, verbose, debug):
    print("Establishing serial communication...")
    time.sleep(2)
    for i in range(5):
        if (send_package(cap, arduino, "99999", verbose, debug)):
            print("Serial communication established")
            return True
    print("Serial communication failed")
    return False