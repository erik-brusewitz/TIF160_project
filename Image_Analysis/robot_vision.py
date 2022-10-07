from Shape_detection import *
import time
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW) #cv2.CAP_DSHOW is used to reduce the time taken to open the ext. camera

while True:
    ret, frame = cap.read()
    coord_matrix = Shape_dectection(frame,'Hexagon')
    cv2.imshow('shapes', frame)
    if cv2.waitKey(1) == ord('q'):
        break
   
cap.release()
cv2.destroyAllWindows()
    

#nothing beyong line 4 works because it is in a loop for as long as the camera is on. 
#this is a problem because python works in a serial manner and we need to implement functions parallely