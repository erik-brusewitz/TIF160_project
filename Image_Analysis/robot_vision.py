from Shape_detection import *
import time

cap = cv2.VideoCapture(1,cv2.CAP_DSHOW) #cv2.CAP_DSHOW is used to reduce the time taken to open the ext. camera

while True:
    if (coord_matrix = Shape_dectection(frame,'Hexagon') == -1):
        print("Exiting ...")
        cap.release()
        cv2.destroyAllWindows()
    
    #return coord_matrix
    

    time.sleep(0.7)