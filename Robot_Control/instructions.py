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
    hubert.move("shoulder", 4*pi/9)
    hubert.move("elbow", -3*pi/18)
    hubert.move("wrist", 0)
    hubert.move("gripper", 0)
    hubert.move("head", pi/2)

def find_shape(hubert, shape):
    print("Searching for " + shape + "...")
    hubert.move("body", 0)
    #hubert.move("head", pi/4)
    for i in range(17):
        coordinate_data = vision.Shape_dectection(shape)
        if coordinate_data[0] != [2,2]:
            print("Found a " + shape)
            return True
        hubert.move("body", pi*i/32) # we can use head 
    print(shape + " not found")
    find_shape(shape)
    
def find_hand(hubert):
    print("Searching for hand...")
    a = hubert.get_angle("body")
    b = hubert.get_angle("head")
    
def move_hand_to_position(hubert, hand_pos, target_pos):
    
    dirc = direction(hubert)

    dirc.motion(hand_pos,target_pos)
    return True
    
def find_container(hubert, shape):
    print("Searching for container to " + shape + "...")
    hubert.move("body", pi)
    for i in range(16):
        #container_coordinaates = vision.get_container_coordinates(shape)
        container_coordinaates = Shape_dectection(shape) #temp, will not work, need specific get_container_coordinates function
        
        if container_coordinaates != [2,2]:
            print("Found container for " + shape)
            return True
        hubert.move("body", pi - pi*i/32)
    print("Container for " + shape + " not found")
    find_container(shape)
    
    
def get_shape(cap, hubert, shape):

    #set_default_position(hubert)
    
    print("Searching for " + shape + "...")
    coordinate_data = vision.get_shape_coordinates(cap, shape)
    hand_coordinates = coordinate_data[0]
    shape_coordinates = coordinate_data[1]
    
    if shape_coordinates == [2,2]:
        find_shape(shape)
        
    coordinate_data = vision.get_shape_coordinates(cap, shape)
    hand_coordinates = coordinate_data[0]
    shape_coordinates = coordinate_data[1]
        
    if hand_coordinates == [2,2]:
        find_hand() #todo
        
    coordinate_data = vision.get_shape_coordinates(cap, shape)
    hand_coordinates = coordinate_data[0]
    shape_coordinates = coordinate_data[1]
    
    if move_hand_to_position(hubert, hand_coordinates, shape_coordinates): #todo
        print("Gripping shape...")
        hubert.move("gripper", 0.9)
        hubert.move("shoulder", 0.1)
        hubert.move("elbow", 7*pi/36)
        hubert.move("body", pi)
        print("Looking for correct container...")
        #container_coordinaates = vision.get_container_coordinates(shape)
        container_coordinaates = vision.get_container_coordinates(cap, shape)
        if container_coordinaates == [2,2]:
            find_container()
            
        #container_coordinaates = vision.get_container_coordinates(shape)
        container_coordinaates = vision.get_container_coordinates(cap, shape)
        print("Dropping shape in container...")
        move_hand_to_position(hubert,hand_coordinates, container_coordinaates)
        hubert.move("gripper", 0)
        
        print("#################")
        print(shape + " was put into the correct container, moving on to the next shape")
        print("#################")