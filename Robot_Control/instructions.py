import Robot_Control.robotControl as rob
import Image_Analysis.robot_vision as vision
import time
import serial
from math import *
from inverseKinematic import *
from gripping import *
import cv2

def initialize_robot(cap, serial_port, verbose, debug):
    if verbose: print("Initializing robot software...")
    print("Initializing arduino with serial port " + serial_port)
    try:
        arduino = serial.Serial(port=serial_port, baudrate=57600, timeout=.1)
    except:
        print("Failed to reach arduino with serial port " + serial_port + ", check for spelling errors and try reconnecting the arduino USB-cable.")
        print("Exiting program...")
        exit()
    rob.sc.initialize_communication(cap, arduino, verbose, debug)
    return rob.robot(cap, arduino, verbose, debug)

def set_default_position(hubert):
    print("Setting Hubert to default position...")
    hubert.move("body", pi/2)
    hubert.move("elbow", -50*pi/180)
    hubert.move("shoulder", 88*pi/180)
    hubert.move("wrist", 0)
    hubert.move("gripper", 0)
    hubert.move("head", pi/2)


def search_for_shape(hubert, shape, cap, verbose, debug):
    if not vision.is_shape_detected(cap, shape, verbose, debug):
        print("Shape not detected!")
        k = False
        print("Searching for " + shape + "...")
        for i in range(11):
            hubert.move("body", pi/2 + i*pi/20)
            if vision.is_shape_detected(cap, shape, verbose, debug):
                if k == True or i == 10:
                    print("Shape found!")
                    return True
                else:
                    if verbose: print(shape + " in frame, confirming...")
                    k = True
        print(shape + " not found, trying again...")
        return search_for_shape(hubert, shape, cap, verbose, debug)

    else:
        return True
    
def search_for_hand(hubert, cap, shape, verbose, debug): #Temp code, is never needed   
    if vision.get_shape_coordinates(cap, shape, verbose, debug) == 444: #hand not found
        print("Hand not found!")
        print("Searching for hand...")
        a = hubert.get_angle("body")
        b = hubert.get_angle("head")
        return search_for_hand(hubert, cap, shape, verbose, debug)
    else: #is run when the hand is found
        return True


def move_arm_and_grab_shape(hubert, cap, shape, verbose, debug):
    if move_arm_to_shape(hubert, cap, shape, verbose, debug):
        print("Gripping shape...")
        if grip_shape(hubert, shape, verbose, debug):
            return True
        else:
            move_arm_and_grab_shape(hubert, cap, shape, verbose, debug)

    
def move_arm_to_shape(hubert, cap, shape, verbose, debug):
    search_for_hand(hubert, cap, shape, verbose, debug)
    search_for_shape(hubert, shape, cap, verbose, debug)
    while True:
        print("Moving hand towards " + shape + "...")
        coordinate_data = vision.get_shape_coordinates(cap, shape, verbose, debug)
        hand_coordinates = coordinate_data[0]
        shape_coordinates = coordinate_data[1]

        if (shape_coordinates == [8888,8888]): #shape found
            print("Position of " + shape + " reached!")
            return True

        if (move_hand_to_position(hubert, hand_coordinates, shape_coordinates, verbose, debug)):
            print("Small movement successful!")
        else:
            print("Moving arm failed")
            print("Adjusting position slightly and trying again...")
            close_pos = hand_coordinates.copy() * 0.95
            if not move_hand_to_position(hubert, hand_coordinates, close_pos, verbose, debug):
                close_pos = hand_coordinates.copy() * 1.1
                move_hand_to_position(hubert, hand_coordinates, close_pos, verbose, debug)


def move_hand_to_position(hubert, hand_pos, target_pos, verbose, debug):
    if verbose: print("Moving hand...")
    if debug: print("Hand at position (" + str(hand_pos[0]) + ", " + str(hand_pos[1]) + ")\nTarget position: (" + str(target_pos[0]) + ", " + str(target_pos[1]) + ")")

    vector_length = 2
    z_lower = 0.14
    z_upper = 0.17
    dirc = direction(hubert, z_lower, z_upper, verbose, debug)

    error_values = [0.01, 0.02, 0.03, 0.005, 0.001, 0.0001]

    for i in range(len(error_values)):
        if (verbose): print("Trying to find solution for error value " + str(error_values[i]))
        if (dirc.motion(hand_pos,target_pos, error_values[i]) == -1):
            if (verbose): print("Failed to find solution")
        else:
            if verbose: print("Solution found!")
            return True

    return False


def grip_shape(hubert, shape, verbose, debug):
    print("Gripping " + shape + "...")

    grp = grip(hubert, verbose, debug)
    error_values = [0.01, 0.02, 0.03, 0.005, 0.001, 0.0001]

    for i in range(len(error_values)):
        if (verbose): print("Trying to find solution for error value " + str(error_values[i]))
        if (grp.motion(error_values[i]) == -1):
            if (verbose): print("Failed to find solution")
        else:
            if verbose: print("Solution found!")
            return True
    print("Shape is not in reach of the robot. Restarting program...")
    return False
    

def move_arm_and_drop_shape_in_container(hubert, shape, verbose, debug):
    print("Moving shape to container for " + shape + "...")
    hubert.move("elbow", -50*pi/180)
    hubert.move("shoulder", 88*pi/180)

    if (shape == "Quadrilateral"):
        hubert.move("body", 50*pi/180)
        hubert.move("elbow", 0*pi/180)
        hubert.move("shoulder", 50*pi/180)
    elif (shape == "Pentagon"):
        hubert.move("body", 35*pi/180)
        hubert.move("elbow", -50*pi/180)
        hubert.move("shoulder", 88*pi/180)
    elif (shape == "Hexagon"):
        hubert.move("body", 10*pi/180)
        hubert.move("elbow", -50*pi/180)
        hubert.move("shoulder", 88*pi/180)
    else:
        print("Invalid shape, exiting...")
        return False

    print("Dropping shape in container...")
    hubert.move("gripper", 0)
    return True

def get_shape(cap, hubert, shape, verbose, debug):
    print("Initializing search for " + shape + "...")

    search_for_hand(hubert, cap, shape, verbose, debug)
    search_for_shape(hubert, shape, cap, verbose, debug)
    move_arm_and_grab_shape(hubert, cap, shape, verbose, debug)
    move_arm_and_drop_shape_in_container(hubert, shape, verbose, debug)
    set_default_position(hubert)

    print("#################")
    print(shape + " was put into the correct container, moving on to the next shape")
    print("#################")
    return True
