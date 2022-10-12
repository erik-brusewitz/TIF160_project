from Image_Analysis.Shape_detection import *

def Initialize_camera(verbose, debug):
    print("Initializing camera...")
    if verbose:
        print("Trying capture settings: ''-1,cv2.CAP_DSHOW''")
    cap = cv2.VideoCapture(-1,cv2.CAP_DSHOW) #cv2.CAP_DSHOW is used to reduce the time taken to open the ext. camera
    #cap = cv2.VideoCapture(1,"/dev/video0")
    #cap = cv2.VideoCapture(-1)
    if not cap.isOpened():
        if verbose:
            print("Failed, trying capture settings: ''0,cv2.CAP_DSHOW''")
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        
    if not cap.isOpened():
        if verbose:
            print("Failed, trying capture settings: ''1,cv2.CAP_DSHOW''")
        cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
        
    if not cap.isOpened():
        if verbose:
            print("Failed, trying capture settings: ''-1''")
        cap = cv2.VideoCapture(-1)
        
    if not cap.isOpened():
        if verbose:
            print("Failed, trying capture settings: ''0''")
        cap = cv2.VideoCapture(0)
        
    if not cap.isOpened():
        if verbose:
            print("Failed, trying capture settings: ''1''")
        cap = cv2.VideoCapture(1)    
        
    if not cap.isOpened():    
        print("Failed to open camera")
        print("Exiting program...")
        exit()
        
    return cap
    
def get_shape_coordinates(cap, shape):
        
    coord_matrix = Shape_dectection(cap, shape, verbose, debug)
    # if (coord_matrix == [9999,9999]):
        # print("Failed to get shape coordinates")
        # print("Exiting program")
        # cap.release()
        # cv2.destroyAllWindows()
        # exit()
    
    return coord_matrix
    
#at the moment, this is the same as the get_shape_coordinates. Should probably be changed a bit so the robot can differentiate shapes from containers.
def get_container_coordinates(cap, shape):
        
    coord_matrix = Shape_dectection(cap, shape, verbose, debug)
    # if (coord_matrix == [9999,9999]):
        # print("Failed to get container coordinates")
        # print("Exiting program")
        # cap.release()
        # cv2.destroyAllWindows()
        # exit()
    
    return coord_matrix