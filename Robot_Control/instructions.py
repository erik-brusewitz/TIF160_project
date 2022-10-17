import Robot_Control.robotControl as rob
import Image_Analysis.robot_vision as vision
import time
import serial
from math import *
from inverseKinematic import *
from gripping import *
import cv2

def initialize_robot(cap, serial_port, verbose, debug):

    if verbose:
        print("Initializing robot software...")
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
    hubert.move("elbow", 10*pi/180)
    hubert.move("shoulder", 30*pi/180)
    hubert.move("wrist", 0)
    hubert.move("gripper", 0)
    hubert.move("head", pi/2)

def search_for_shape(hubert, shape, cap, verbose, debug):
    k = False
    print("Searching for " + shape + "...")
    for i in range(11):
        hubert.move("body", pi/2 + i*pi/20)
        if vision.Search_for_shape(cap, shape, verbose, debug):
            if k == True or i == 10:
                print("Shape found!")
                return True
            else:
                if verbose: print(shape + " in frame, confirming...")
                k = True
    print(shape + " not found, trying again...")
    return search_for_shape(hubert, shape, cap, verbose, debug)
    
def search_for_hand(hubert):
    print("Searching for hand...")
    a = hubert.get_angle("body")
    b = hubert.get_angle("head")

def move_arm_and_grab_shape(hubert, cap, shape, verbose, debug):
    if move_arm_to_shape(hubert, cap, shape, verbose, debug):
        print("Gripping shape...")
        if grip_shape(hubert, shape, verbose, debug):
            return True
        else:
            move_arm_and_grab_shape(hubert, cap, shape, verbose, debug)

    
def move_arm_to_shape(hubert, cap, shape, verbose, debug):
    
    while True:

        coordinate_data = vision.get_shape_coordinates(cap, shape, verbose, debug)
        hand_coordinates = coordinate_data[0]
        shape_coordinates = coordinate_data[1]

        if (shape_coordinates == [8888,8888]): #shape found
            print("Shape position reached!")
            return True

        if (move_hand_to_position(hubert, hand_coordinates, shape_coordinates, verbose, debug)):

            if hand_coordinates == [4444,4444]: #hand not found
                coordinate_data = search_for_hand(hubert) #todo: move the head to forward position, or untill hand is found (maybe move hand a bit). This function shouldnt be needed.
            
            if shape_coordinates == [7777,7777]: #shape not found
                coordinate_data = search_for_shape(hubert, shape, cap, debug, verbose)
            
        

def move_hand_to_position(hubert, hand_pos, target_pos, verbose, debug):
    
    if verbose:
        print("Moving hand to position...")
        print("Hand at position (" + str(hand_pos[0]) + ", " + str(hand_pos[1]) + ")\nTarget position: (" + str(target_pos[0]) + ", " + str(target_pos[1]) + ")")
    #step = 0.1
    vector_length = 2
    dirc = direction(hubert, vector_length, verbose, debug)

    error_values = [0.01, 0.02, 0.03, 0.005, 0.001, 0.0001]

    for i in range(len(error_values)):
        if (verbose): print("Trying to find solution for error value " + str(error_values[i]))
        if (dirc.motion(hand_pos,target_pos, error_values[i]) == -1):
            if (verbose): print("Failed to find solution")
        else:
            if verbose: print("Solution found!")
            return True
    print("Moving arm failed, trying again...")
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
    
def search_for_container(cap, hubert, shape, verbose, debug):
    print("Searching for container to " + shape + "...")
    hubert.move("body", pi)
    for i in range(16):
        #container_coordinaates = vision.get_container_coordinates(shape)
        container_data = vision.get_container_coordinates(cap, shape, verbose, debug)
        container_coordinates = container_data[1]
        if container_coordinates != [9999,9999]:
            print("Found container for " + shape)
            return container_coordinates
        hubert.move("body", pi - pi*i/32)
    print("Container for " + shape + " not found")
    container_coordinates = search_for_container(hubert, shape, verbose, debug)
    
    
def get_shape(cap, hubert, shape, verbose, debug):

    #set_default_position(hubert)
    
    print("Initializing search for " + shape + "...")
    search_for_shape(hubert, shape, cap, verbose, debug)

    coordinate_data = vision.get_shape_coordinates(cap, shape, verbose, debug)
    hand_coordinates = coordinate_data[0]
    shape_coordinates = coordinate_data[1]
   
    if hand_coordinates == [9999,9999]:
        if verbose: print("Hand not found, searching for hand...")
        coordinate_data = search_for_hand(hubert) #todo: move the head to forward position, or untill hand is found (maybe move hand a bit). This function shouldnt be needed.
    
    if shape_coordinates == [9999,9999]:
        coordinate_data = search_for_shape(hubert, shape, cap, debug, verbose)
        hand_coordinates = coordinate_data[0]
        shape_coordinates = coordinate_data[1]

    move_arm_and_grab_shape(hubert, cap, shape, verbose, debug)

    print("Looking for correct container...")
    container_data = vision.get_container_coordinates(cap, shape, verbose, debug) #container data contains both the hand and the container coordinates
    hand_coordinates = container_data[0]
    container_coordinates = container_data[1]
    if container_coordinates == [9999,9999]:
        container_coordinates = search_for_container(cap, hubert, shape, verbose, debug)

    print("Dropping shape in container...")
    #move_hand_to_position(hubert, cap, shape, hand_coordinates, container_coordinates, verbose, debug)
    hubert.move("gripper", 0)
    
    print("#################")
    print(shape + " was put into the correct container, moving on to the next shape")
    print("#################")
    return True
