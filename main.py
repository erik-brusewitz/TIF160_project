#import Robot_Control.instructions as instructions
#import Robot_Control.instructions.vision as vision
from Robot_Control import instructions
from Image_Analysis import robot_vision as vision
import argparse

def main():

    parser = argparse.ArgumentParser(description="Parsing command line arguments...")
    #parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
    #parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')
    
    parser.add_argument("port", help="The arduino communications port")

    
    args = parser.parse_args()
    
    if args.port:
        print("Port is set to " + args.port)
        serial_port = args.port
    else:
        print("Port not set, setting to 0")
        serial_port = "0"
        
    #print(args.accumulate(args.integers))
    
    
    hubert = instructions.initialize_robot(serial_port)
    cap = vision.Initialize_camera()
    
    if (hubert == -1 || cap == -1):
        throw(error)
    
    
    shapes = ["Quadrilateral", "Pentagon", "Hexagon"]
    for shape in shapes:
        shape = "Hexagon"
        instructions.get_shape(cap, hubert, shape)
    instructions.set_default_position(hubert)
    print("All shapes have been put into the correct containers. Program is finished")

if __name__ == "__main__":
    main()