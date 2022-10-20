import cv2

cam = cv2.VideoCapture(1,cv2.CAP_DSHOW)

focus = 40  # min: 0, max: 255, increment:5
cam.set(28, focus)

while True:
        ret, frame = cam.read()
        cv2.imshow('shapes', frame)
        
        if cv2.waitKey(1) == ord('q'):
            print("Camera exited manually")