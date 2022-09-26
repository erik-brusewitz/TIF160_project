import Robot_Control.instructions as instructions

def main():
    
    hubert = instructions.initialize_robot()
    shapes = ["Quadrilateral", "Pentagon", "Hexagon"]
    for shape in shapes:
        instructions.get_shape(hubert, shape)
    instructions.set_default_position(hubert)
    print("All shapes have been put into the correct containers. Program is finished")

if __name__ == "__main__":
    main()