import numpy as np
import cv2, math
from Image_Analysis.color_detection import *

def Shape_dectection():
    cap = cv2.VideoCapture(1,cv2.CAP_DSHOW) #cv2.CAP_DSHOW is used to reduce the time taken to open the ext. camera
    if not cap.isOpened():
        print("Cannot open camera")
        exit()


    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        imgGry = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  

        thrash  = cv2.adaptiveThreshold(imgGry, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 8)
        contours , _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        i = 0
        coord_matrix=[[],[]]
        (color_centre_x, color_centre_y) = color_detection(frame)
        arm_coord=[color_centre_x,color_centre_y]
        coord_matrix[0]=arm_coord
        # print(arm_coord)
        # list for storing names of shapes
        for contour in contours:
        
            # here we are ignoring first counter because 
            # findcontour function detects whole image as shape
            if i == 0:
                i = 1
                continue
        
            # cv2.approxPloyDP() function to approximate the shape
            approx = cv2.approxPolyDP(
                contour, 0.01 * cv2.arcLength(contour, True), True)
            

            # finding center point of shape
            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])

            for aa in approx:
                dist= math.sqrt((aa[0][0]-x)**2+(aa[0][1]-y)**2)
                if dist >=35:
                    # using drawContours() function
                    cv2.drawContours(frame, [contour], 0, (0, 0, 255), 3)

                    # putting shape name at center of each shape
                    if len(approx) == 3:
                        cv2.putText(frame, 'Triangle', (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                    elif len(approx) == 4:
                        cv2.putText(frame, 'Quadrilateral', (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                        quad_x=x; quad_y=y
                        quad_c=[quad_x,quad_y]
                        coord_matrix[1]=quad_c

                    elif len(approx) == 5:

                        cv2.putText(frame, 'Pentagon', (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
                    elif len(approx) == 6:
                        cv2.putText(frame, 'Hexagon', (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
                    else:
                        if dist <= 120:
                            cv2.putText(frame, 'ARM', (x, y),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        print(coord_matrix)    

        cv2.imshow('shapes', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return(coord_matrix)