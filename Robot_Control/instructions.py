import Robot_Control.robotControl as rob
import Image_Analysis.robot_vision as vision
import time
import serial
from math import *
from inverseKinematic import *

def initialize_robot(serial_port, verbose, debug):

    if verbose:
        print("Initializing robot software...")
    print("Initializing arduino with serial port " + serial_port)
    try:
        arduino = serial.Serial(port=serial_port, baudrate=57600, timeout=.1)
    except:
        print("Failed to reach arduino with serial port " + serial_port + ", check for spelling errors and try reconnecting the arduino USB-cable.")
        print("Exiting program...")
        exit()

    rob.sc.initialize_communication(arduino, verbose, debug)
    return rob.robot(arduino, verbose, debug)

def set_default_position(hubert):
    print("Setting Hubert to default position...")
    hubert.move("body", pi/2)
    hubert.move("elbow", 10*pi/180)
    hubert.move("shoulder", 30*pi/180)
    hubert.move("wrist", 0)
    hubert.move("gripper", 0)
    hubert.move("head", pi/2)

def search_for_shape(hubert, shape, cap, verbose, debug):
    print(shape + " not found, searching...")
    hubert.move("body", pi/2)
    for i in range(17):
        coordinate_data = vision.get_shape_coordinates(cap, shape, verbose, debug)
        if coordinate_data[1] != [9999,9999]:
            print("Found a " + shape)
            return coordinate_data
        hubert.move("body", pi/2 + i*pi/32) # we can use head 
    coordinate_data = search_for_shape(hubert, shape, cap, verbose, debug)
    return coordinate_data
    
def search_for_hand(hubert):
    print("Searching for hand...")
    a = hubert.get_angle("body")
    b = hubert.get_angle("head")
    
def move_hand_to_position(hubert, cap, shape, hand_pos, target_pos, verbose, debug):
    if verbose:
            print("Trying to move hand towards object position...")
            print("Hand at position (" + str(hand_pos[0]) + ", " + str(hand_pos[1]) + ")\Object position: (" + str(target_pos[0]) + ", " + str(target_pos[1]) + ")")
    while True:
        if (move_hand_towards_position(hubert, hand_pos, target_pos, verbose, debug)):
            coordinate_data = vision.get_shape_coordinates(cap, shape, verbose, debug)
            hand_coordinates = coordinate_data[0]
            shape_coordinates = coordinate_data[1]
        
            if hand_coordinates == [9999,9999]:
                if verbose: print("Hand not found, searching for hand...")
                coordinate_data = search_for_hand(hubert) #todo: move the head to forward position, or untill hand is found (maybe move hand a bit). This function shouldnt be needed.
            
            if shape_coordinates == [9999,9999]:
                coordinate_data = search_for_shape(hubert, shape, cap, debug, verbose)
            
            hand_pos = coordinate_data[0]
            target_pos = coordinate_data[1]

        if (target_pos == [8888,8888]):
            print("Shape position reached!")
            return True

def move_hand_towards_position(hubert, hand_pos, target_pos, verbose, debug):
    
    if verbose:
        print("Trying to move hand to position...")
        print("Hand at position (" + str(hand_pos[0]) + ", " + str(hand_pos[1]) + ")\nTarget position: (" + str(target_pos[0]) + ", " + str(target_pos[1]) + ")")
    step = 0.1
    vector_length = 2
    dirc = direction(hubert, step, vector_length, verbose, debug)
    if (dirc.motion(hand_pos,target_pos) == -1):
        print("Failed to find solution, trying with step 0.001")
        step = 0.001
        dirc = direction(hubert, step, vector_length, verbose, debug)

    if (dirc.motion(hand_pos,target_pos) == -1):
        print("Failed to find solution, trying with step 0.0001")
        step = 0.0001
        dirc = direction(hubert, step, vector_length, verbose, debug)

    if (dirc.motion(hand_pos,target_pos) == -1):
        print("Failed to find solution with step 0.0001, try moving the shape closer to the robot.")
        print("Pausing program for 5 seconds...")
        time.sleep(5)
        return False

    return True
    
def search_for_container(hubert, shape, verbose, debug):
    print("Searching for container to " + shape + "...")
    hubert.move("body", pi)
    for i in range(16):
        #container_coordinaates = vision.get_container_coordinates(shape)
        container_coordinaates = vision.get_container_coordinates(cap, shape, verbose, debug)
        if container_coordinaates != [9999,9999]:
            print("Found container for " + shape)
            return container_coordinates
        hubert.move("body", pi - pi*i/32)
    print("Container for " + shape + " not found")
    container_coordinates = search_for_container(hubert, shape, verbose, debug)
    
    
def get_shape(cap, hubert, shape, verbose, debug):

    #set_default_position(hubert)
    
    print("Searching for " + shape + "...")
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

    while True:
        if move_hand_to_position(hubert, cap, shape, hand_coordinates, shape_coordinates, verbose, debug):

            print("Gripping shape...")
            hubert.move("gripper", 0.9)
            hubert.move("shoulder", 0.1)
            hubert.move("elbow", 7*pi/36)
            hubert.move("body", pi)
            print("Looking for correct container...")
            container_coordinaates = vision.get_container_coordinates(cap, shape, verbose, debug)
            if container_coordinaates[1] == [9999,9999]:
                container_coordinates = search_for_container(hubert, shape, verbose, debug)
                
            #container_coordinaates = vision.get_container_coordinates(shape)
            container_coordinaates = vision.get_container_coordinates(cap, shape, verbose, debug)
            print("Dropping shape in container...")
            move_hand_to_position(hubert, cap, shape, hand_coordinates, container_coordinaates, verbose, debug)
            hubert.move("gripper", 0)
            
            print("#################")
            print(shape + " was put into the correct container, moving on to the next shape")
            print("#################")
            return True

        else:
            print("Trying again...")
