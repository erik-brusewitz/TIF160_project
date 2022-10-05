import Robot_Control.instructions as instructions
import instructions.vision as vision
import argparse

def main():

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))
    
    
    hubert = instructions.initialize_robot()
    cap = vision.Initialize_camera()
    shapes = ["Quadrilateral", "Pentagon", "Hexagon"]
    for shape in shapes:
        shape = "Hexagon"
        instructions.get_shape(cap, hubert, shape)
    instructions.set_default_position(hubert)
    print("All shapes have been put into the correct containers. Program is finished")

if __name__ == "__main__":
    main()