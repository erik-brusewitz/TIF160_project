from Image_Analysis.Shape_detection import *

def Initialize_camera():

    cap = cv2.VideoCapture(1,cv2.CAP_DSHOW) #cv2.CAP_DSHOW is used to reduce the time taken to open the ext. camera
    if not cap.isOpened():
        print("Cannot open camera")
        return -1
    return cap
    
def get_shape_coordinates(cap, shape):
        
    coord_matrix = Shape_dectection(cap, shape)
    if (coord_matrix == -1):
        print("Exiting ...")
        cap.release()
        cv2.destroyAllWindows()
        return -1
    
    return coord_matrix
    
#at the moment, this is the same as the get_shape_coordinates. Should probably be changed a bit so the robot can differentiate shapes from containers.
def get_container_coordinates(cap, shape):
        
    coord_matrix = Shape_dectection(cap, shape)
    if (coord_matrix == -1):
        print("Exiting ...")
        cap.release()
        cv2.destroyAllWindows()
        return -1
    
    return coord_matrix