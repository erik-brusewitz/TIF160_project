from math import *
import time
import serial
from Robot_Control import serialCommunication as sc

# class that is used to control the servo motor of the robot,
# it has different function:
# - .info() to get the information about the servo 
# - .move( angle ) move the servo to that specific angle
class servo:
    def __init__(self, cap, arduino, verbose, debug, servo_id, minPosition, maxPosition, minAngle, maxAngle, flip_angle_direction):
        self.cap = cap
        self.arduino = arduino
        self.verbose = verbose
        self.debug = debug
        self.servo_id = servo_id
        self.minPosition = minPosition
        self.maxPosition = maxPosition
        self.range = abs(maxAngle - minAngle)
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.currentAngle = minAngle #default is set to minAngle, should probably be something else?
        self.flip_angle_direction = flip_angle_direction

    def info(self):
        print("servo_id:", self.servo_id, "\nMin Angle: ", self.minAngle, "\nMax Angle: ", self.maxAngle, "\nMin Position:", self.minPosition, "\nMax Position: ", self.maxPosition, "\nCurrent Angle: ", self.currentAngle)

    def move(self, newAngle):

        oldAngle = self.currentAngle

        if self.debug: self.info()
        tmp = newAngle - self.minAngle
        if self.flip_angle_direction:
            self.position = int(self.maxPosition - (tmp / self.range) * ( self.maxPosition - self.minPosition))
        else:
            self.position = int(self.minPosition + (tmp / self.range) * ( self.maxPosition - self.minPosition))
            
        position_string = str(self.position)
        if self.position < self.minPosition or self.position > self.maxPosition:
            print("Error, position = " + str(self.position) + ", expected value between " + str(self.minPosition) + " and " + str(self.maxPosition))
            return 0
        if self.position < 1000:
            sc.send_package(self.cap, self.arduino, str(self.servo_id) + "0" + str(self.position), self.verbose, self.debug)
        else:
            sc.send_package(self.cap, self.arduino, str(self.servo_id) + str(self.position), self.verbose, self.debug)
        if self.debug:
            print('End the communication to move servo')
        self.currentAngle = newAngle

        #sleepTime = 0.3 * abs(newAngle - oldAngle)
        #if (self.debug): print("Sleeping for " + str(sleepTime) + " seconds")
        #time.sleep(sleepTime)
            
        return 0
        
    def get_angle(self):
        return self.currentAngle

# //Servos
# //Servo body; //id 0, pin number 3, min 560, max 2330
# //Servo shoulder; //id 1, pin number 9, min 750, max 2200
# //Servo elbow; //id 2, pin number 10, min 550, max 2400
# //Servo wrist; //id 3, pin number 6, min 950, 2400
# //Servo gripper; //id 4, pin number 11, min 550, max 2150
# //Servo head; //id 5, pin number 5, min 550, max 2340

# the class robot contain the information about alla the servo motor of the robot and also controll them.
# .info( "motor name" ) give the infomation about that specif servo 
# .move( "motor name", angle ) move that specific servo to that angle
class robot:
    def __init__(self, cap, arduino, verbose, debug):
        self.cap = cap
        self.arduino = arduino
        self.verbose = verbose
        self.debug = debug
        #self.arduino = serial.Serial(port='COM5', baudrate=57600, timeout=.1)
        if verbose:
            print("Initializing servos...")
        self.bodyMotor = servo(self.cap, self.arduino,self.verbose,self.debug,0,560,2330,0,pi,1) #0 is left facing, pi is right facing
        self.shoulderMotor = servo(self.cap, self.arduino,self.verbose,self.debug,1,750,2200,0,160*pi/180,1) #0 is down, 8*pi/9 (160 degrees) is up
        self.elbowMotor = servo(self.cap, self.arduino,self.verbose, self.debug,2,550,1600,-50*pi/180,35*pi/180,0) # -50 degrees i backwards, +35 degrees is forwards. (1100 is 0 degrees, 2400 is the max value, but the servo cant handle higher than 1600 = 35 degrees.)
        self.wristMotor = servo(self.cap, self.arduino,self.verbose, self.debug,3,550,2400,-39.6*pi/180,140.4*pi/180,0) #-22pi is close to the 0 positon at 950, then it rotates counter clockwise when moving to 0.78pi.
        self.gripperMotor = servo(self.cap, self.arduino,self.verbose, self.debug,4,550,2150,0,1,0) #0 is open, 1 is closed
        self.headMotor = servo(self.cap, self.arduino,self.verbose, self.debug,5,550,2340,0,pi,1) #0 is left, pi is right

    def __motorC(self, motor):
        if ( motor == 'body'):
            r = self.bodyMotor
        elif ( motor == 'shoulder'):
            r = self.shoulderMotor
        elif ( motor == 'elbow'):
            r = self.elbowMotor
        elif ( motor == 'wrist'):
            r = self.wristMotor
        elif ( motor == 'gripper'):
            r = self.gripperMotor
        elif ( motor == 'head'):
            r = self.headMotor
        else: 
            r = 1
        return r


    def move(self, motor, angle):
        r = self.__motorC(motor)
        #print(motor)
        
        if r != 1:
            r.move(angle)
        else: 
            return 1
    
    def info(self, motor):
        r = self.__motorC(motor)
        
        if r != 1:
            print('Info of %s servo' % motor)
            r.info()
        else: 
            return 1
            
    def get_angle(self, motor):
        r = self.__motorC(motor)
        return r.get_angle()