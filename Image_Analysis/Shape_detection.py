from typing import final
import numpy as np
import cv2, math
from Image_Analysis.color_detection import *
#from color_detection import * #for ash's local computer

def Shape_dectection(cap,shape,pick_up,verbose,debug):
    #If pick_up is 1, then the camera should find a shape to pick up
    #If pick_up is 0, the camera should find the container coordinates (centre)
    if not cap.isOpened():
        print("Cannot open camera")
        return -1

    
    ret, frame = cap.read()
    
    #cv2.imwrite("preview.jpg", frame)
    
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?)")
        return -1

    # cv2.imshow('shapes', frame)
    # if cv2.waitKey(1) == ord('q'):
    #     print("Camera exited manually")
    #     return -1
    
    ret, frame = cap.read()
    cv2.imshow('shapes', frame)
    if cv2.waitKey(1) == ord('q'):
        print("Camera exited manually")
        return -1
    print("Program should wait for user input...")
    #cv2.waitKey(0)
    ret, frame = cap.read()
    cv2.imshow('shapes', frame)
    cv2.waitKey(1)
    print("Program continuing...")

    
    imgGry = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  

    thrash  = cv2.adaptiveThreshold(imgGry, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 8)
    contours , _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    i = 0
    coord_matrix=[[],[],[]]
    
    (arm_coord,closest_red)=color_detection(frame)
    coord_matrix[0] = arm_coord

    if arm_coord == []: return [4444,4444] #hand not found

    coord_matrix[2] = closest_red
    if closest_red == [8888,8888]:
        distance_between_red_and_green = 8888
    else:
        distance_between_red_and_green = math.sqrt((arm_coord[0] - closest_red[0])**2+(arm_coord[1] - closest_red[1])**2)
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
                quad_c = None
                if dist >=35:
                    # using drawContours() function
                    cv2.drawContours(frame, [contour], 0, (0, 0, 255), 3)

                    #putting shape name at center of each shape

                    if len(approx) == 4:
                        cv2.putText(frame, 'Quadrilateral', (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                        if shape == 'Quadrilateral':
                            quad_x=x; quad_y=y
                            quad_c=[quad_x/640,quad_y/480]   
                            coord_matrix[1]=(quad_c)


                    elif len(approx) == 5:

                        cv2.putText(frame, 'Pentagon', (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                        if shape =='Pentagon':
                            pent_x=x; pent_y=y
                            pent_c=[pent_x/640,pent_y/480]
                            coord_matrix[1] = pent_c
            

                    elif len(approx) == 6:
                        cv2.putText(frame, 'Hexagon', (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                        if shape =='Hexagon':
                            hexa_x=x; hexa_y=y
                            hexa_c=[hexa_x/640,hexa_y/480]
                            coord_matrix[1] = hexa_c
            
                    else:
                        if dist <= 120:
                            cv2.putText(frame, 'ARM', (x, y),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    #print("the op matrix is:" , coord_matrix)    
    #final_cords = arm + destination_matrix [1x2]
    final_cords = [[], []]
    final_cords[0] = arm_coord
    
    print("The distance_between_red_and_green " + str(distance_between_red_and_green)) 
    #once shape stops being recognized, we first check for nearest red color
    if coord_matrix[1] ==[] and distance_between_red_and_green <=0.25:
        final_cords[1] = coord_matrix[2]
#we want to ognore the red from another shape, so any dist more than 0.25 should be avoided/cancelled
    elif coord_matrix[1] ==[] and distance_between_red_and_green > 0.3:
        final_cords[1] = [8888,8888]

#the arm is exactly over the desired location, so we need to pick it up (or could happen when there is no
# other red color on the screen)
    elif coord_matrix[1] ==[] and distance_between_red_and_green == 8888:
        final_cords[1] = [8888,8888]

#arm is over the desired location, pick it up BUT there are more reds around
   
    else:  #as long as the shape is visible
        final_cords[1] = coord_matrix[1]

    #cv2.imshow('shapes', frame)
    
    #if q is pressed with focus on the camera window, the program is stopped.
    #This line is required for the camera window to work, otherwise it crashes.
    #It does not matter what is inside the if statement, the important line is the if statement itself.
    if cv2.waitKey(1) == ord('q'):
        print("Camera exited manually")
        return -1
        
    #print("Three dims: ", coord_matrix)
    if verbose:
        print("Returning object coordinates: ", final_cords)

    return(final_cords)