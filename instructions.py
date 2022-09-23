import robotControl as rob
import Image_Analysis.Shape_detection as vision

def initialize_robot():
    rob.sc.initialize_communication()
    print("Initializing robot software")
    hubert = rob.robot()

def set_default_position():
    hubert.move("body", pi/2)
    hubert.move("shoulder", 4*pi/9)
    hubert.move("elbow", -3*pi/18)
    hubert.move("wrist", 0)
    hubert.move("gripper", 0)
    hubert.move("head", pi/2)

def find_shape(shape):
    print("Searching for " + shape + "...")
    hubert.move("body", pi/2)
    hubert.move("head", pi/4)
    for i in range(16):
        coordinate_data = vision.getCoordinates(shape)
        if coordinate_data[0] != [2,2]:
            print("Found a " + shape)
            return True
        hubert.move("head", pi/4 + pi*i/32)
    print(shape + " not found")
    find_shape(shape)
    
def find_hand():
    print("Searching for hand...")
    
def move_hand_to_position(hand_pos, target_pos):
    
    #put inverse kinematic equations here...
    return True
    
def find_container(shape):
    print("Searching for container to " + shape + "...")
    hubert.move("body", pi)
    for i in range(16):
        container_coordinaates = vision.get_container_coordinates(shape)
        if container_coordinaates != [2,2]:
            print("Found container for " + shape)
            return True
        hubert.move("body", pi - pi*i/32)
    print("Container for " + shape + " not found")
    find_container(shape)
    
    
def get_shape(shape):
   
    set_default_position()
    
    print("Searching for " + shape + "...")
    coordinate_data = vision.getCoordinates(shape)
    hand_coordinates = coordinate_data[0]
    shape_coordinates = coordinate_data[0]
    
    if shape_coordinates == [2,2]:
        find_shape(shape)
        
    coordinate_data = vision.getCoordinates(shape)
    hand_coordinates = coordinate_data[0]
    shape_coordinates = coordinate_data[0]
        
    if hand_coordinates == [2,2]:
        find_hand() #todo
        
    coordinate_data = vision.getCoordinates(shape)
    hand_coordinates = coordinate_data[0]
    shape_coordinates = coordinate_data[0]
    
    if move_hand_to_position(hand_coordinates, shape_coordinates): #todo
        print("Gripping shape...")
        hubert.move("gripper", 0.9)
        hubert.move("shoulder", 0.1)
        hubert.move("elbow", 7*pi/36)
        hubert.move("body", pi)
        print("Looking for correct container...")
        container_coordinaates = vision.get_container_coordinates(shape)
        if container_coordinaates == [2,2]:
            find_container()
            
        container_coordinaates = vision.get_container_coordinates(shape)
        print("Dropping shape in container...")
        move_hand_to_position(hand_coordinates, container_coordinaates)
        hubert.move("gripper, 0")
        
        print("#################")
        print(shape + " was put into the correct container, moving on to the next shape")
        print("#################")