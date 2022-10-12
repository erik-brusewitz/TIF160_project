# Python code for Multiple Color Detection


import numpy as np
import cv2,math

def color_detection(imageFrame):

	hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

	# Set range for red color to kill it and
	# define mask
	red_lower = np.array([136, 87, 111], np.uint8)
	red_upper = np.array([180, 255, 255], np.uint8) #[180, 255, 255],
	red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

	# Set range for green color and
	# define mask
	green_lower = np.array([33.3, 69.3, 96], np.uint8)
	green_upper = np.array([102, 255, 255], np.uint8)
	green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

	# Morphological Transform, Dilation
	# for each color and bitwise_and operator
	# between imageFrame and mask determines
	# to detect only that particular color
	kernal = np.ones((5, 5), "uint8")
	
	# For red color
	red_mask = cv2.dilate(red_mask, kernal)
	res_red = cv2.bitwise_and(imageFrame, imageFrame,
							mask = red_mask)
	
	# For green color
	green_mask = cv2.dilate(green_mask, kernal)
	res_green = cv2.bitwise_and(imageFrame, imageFrame,
								mask = green_mask)
	
	#initialization
	a = b = 0 
	green_color_array=[]
	red_color_matrix = []


	# #GREEN		
	contours, hierarchy = cv2.findContours(green_mask,
										cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)

	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		M = cv2.moments(contour)
		if M['m00'] != 0.0:
			a = int(M['m10']/M['m00']) #finding centre points of the detected color
			b = int(M['m01']/M['m00'])
		
		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			imageFrame = cv2.rectangle(imageFrame, (x, y),
									(x + w, y + h),
									(0, 255, 0), 2)
			#print(" the arm centre is: " , a,b)
			cv2.putText(imageFrame, "Green Colour", (a, b),
						cv2.FONT_HERSHEY_SIMPLEX, 1.0,
						 (0, 255, 0))

			green_color_array.append(a/640)	
			green_color_array.append(b/480)


	# # Creating contour to track red color
	contours, hierarchy = cv2.findContours(red_mask,
										cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
	
	#color_matrix=[]
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		M = cv2.moments(contour)
		if M['m00'] != 0.0:
			a = int(M['m10']/M['m00']) #finding centre points of the detected color
			b = int(M['m01']/M['m00'])

		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			imageFrame = cv2.rectangle(imageFrame, (x, y),
									(x + w, y + h),
									(0, 0, 255), 2)
			#print("The red centre is : ",a,b)
			cv2.putText(imageFrame, "Red Colour", (a,b),
						cv2.FONT_HERSHEY_SIMPLEX, 1.0,
						(0, 0, 255))	

			red_color_matrix.append([a/640,b/480])

	dist_red_green = []
	if len(red_color_matrix) == 0:
		dist_red_green.append(4)
		red_color_matrix.append([3,3])		

	else:
	
		for c in range(len(red_color_matrix)):
				
			if len(green_color_array)==0 or len(red_color_matrix) == 0:
				dist_red_green.append(3)
			else:
				dist_red_green.append(math.sqrt((green_color_array[0] - red_color_matrix[c][0])**2+(green_color_array[1] - red_color_matrix[c][1])**2))
	# print(np.min(dist_red_green))
	# print(dist_red_green)
	# print(dist_red_green.index(np.min(dist_red_green)))
	closest_red = dist_red_green.index(np.min(dist_red_green))
	# print('dist_red_green: ', dist_red_green)
	# print("red matrix is: ", red_color_matrix)
	# # print("cloests red: ", closest_red)
	# print("list: ", dist_red_green)

	# Creating contour to track green color
	if green_color_array !=[]:
		return(green_color_array, red_color_matrix[closest_red])
	else:
		return([9999,9999],[9999,9999])