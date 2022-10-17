#import Robot_Control.instructions as instructions
#import Robot_Control.instructions.vision as vision
from Robot_Control import instructions
from Image_Analysis import robot_vision as vision
import argparse
import time
import cv2

def camera_test(cap):
    while True:
        ret, frame = cap.read()
        cv2.imshow('shapes', frame)
        if cv2.waitKey(1) == ord('q'):
            print("Camera exited manually")
            return -1
#         time.sleep(0.01)
        


def main():
    print("Starting program...")

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-p", "--port", help = "Required argument: sets the arduino communications port")
    parser.add_argument("-v", "--verbose", action = "store_true", help = "Prints more text when running the program")
    parser.add_argument("-d", "--debug", action = "store_true", help = "Prints even more text than verbose, used for debugging")
    args = parser.parse_args()

    verbose = args.verbose
    debug = args.debug
    
    if verbose:
        print("Verbose printing")
    if debug:
        print("Debug printing")
    
    if args.port:
        serial_port = args.port
        print("Serial port is set to " + serial_port)   
    else:
        print("Port not set, defaulting to /dev/ttyACM0")
        #serial_port = "/dev/ttyACM0"
        serial_port = "COM7"
        print("Also setting verbose and debug to true")
        verbose = False
        debug = False
        

    hubert = instructions.initialize_robot(serial_port, verbose, debug)
    if verbose:
        print("Robot initialization successful")
    
    cap = vision.Initialize_camera(verbose, debug) 
    if verbose:
        print("Camera initialization successful")
    #camera_test(cap)

    instructions.set_default_position(hubert)
    
    shapes = ["Quadrilateral", "Pentagon", "Hexagon"]
    print("Searching for the shapes...")
    for shape in shapes:
        instructions.get_shape(cap, hubert, shape, verbose, debug)
    instructions.set_default_position(hubert)
    print("All shapes have been put into the correct containers. Program is finished")

if __name__ == "__main__":
    main()