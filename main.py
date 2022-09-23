import instructions

def main():
    
    instructions.initialize_robot()
    shapes = ["Quadrilateral", "Pentagon", "Hexagon"]
    for shape in shapes:
        instructions.get_shape(shape)
    instructions.set_default_position()
    print("All shapes have been put into the correct containers. Program is finished")

if __name__ == "__main__":
    main()