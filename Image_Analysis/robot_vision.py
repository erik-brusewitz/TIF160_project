from Image_Analysis.Shape_detection import *

def Initialize_camera(verbose, debug):
    print("Initializing camera...")
    if verbose:
        print("Trying capture settings: ''-1''")
    #cap = cv2.VideoCapture(-1,cv2.CAP_DSHOW) #cv2.CAP_DSHOW is used to reduce the time taken to open the ext. camera
    cap = cv2.VideoCapture(1,cv2.CAP_DSHOW) #cv2.CAP_DSHOW is used to reduce the time taken to open the ext. camera
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        if verbose:
            print("Failed, trying capture settings: ''-1,cv2.CAP_DSHOW''")
        cap = cv2.VideoCapture(-1,cv2.CAP_DSHOW)
    
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

def program_exit(cap):
     print("Failed to get shape coordinates")
     print("Exiting program")
     cap.release()
     cv2.destroyAllWindows()
     exit()


def is_shape_detected(cap, shape, verbose, debug):
    search_for_shape = True
    return Shape_dectection(cap, shape, search_for_shape, verbose, debug)


#Return codes from Shape_detection:
# return = -1: camera is not opened or if frame is read incorrectly. Should close the program
# return = True/False: Used for "is shape detected"
# return = 444: hand not found. Search for hand must be run
# return[1] = [6666,6666]: big error. Search for shape should be run
# return[1] = [8888,8888]: Shape not visible and no close red colors. Shape should be picked up

def get_shape_coordinates(cap, shape, verbose, debug):
    search_for_shape = False
    coord_matrix = Shape_dectection(cap, shape, search_for_shape, verbose, debug)
    if (verbose): print(coord_matrix)
    
    if coord_matrix == -1:
        program_exit()
    
    return coord_matrix