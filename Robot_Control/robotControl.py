from math import *
import time
import serial
import Robot_Control.serialCommunication as sc

# class that is used to control the servo motor of the robot,
# it has different function:
# - .info() to get the information about the servo 
# - .move( angle ) move the servo to that specific angle
class servo:
    def __init__(self, arduino, servo_id, minPosition, maxPosition, minAngle, maxAngle):
        self.arduino = arduino
        self.servo_id = servo_id
        self.minPosition = minPosition
        self.maxPosition = maxPosition
        self.range = abs(maxAngle - minAngle)
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.currentAngle = minAngle #default is set to minAngle, should probably be something else?

    def info(self):
        print("servo_id:", self.servo_id, "\nMin Angle: ", self.minAngle, "\nMax Angle: ", self.maxAngle, "\nMin Position:", self.minPosition, "\nMax Position: ", self.maxPosition, "\nCurrent Angle: ", self.currentAngle)

    def move(self, newAngle):
    
        print('Start the communication to move servo')
        tmp = newAngle - self.minAngle
        self.position = int(self.minPosition + (tmp / self.range) * ( self.maxPosition - self.minPosition))
        position_string = str(self.position)
        if self.position < 550 or self.position > 2400:
            print("Error, position is too large or too low")
        if self.position < 1000:
            sc.send_package(self.arduino, str(self.servo_id) + "0" + str(self.position))
        else:
            sc.send_package(self.arduino, str(self.servo_id) + str(self.position))
        print('End the communication to move servo')
        self.currentAngle = newAngle
            
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
    def __init__(self, arduino):
    
        self.arduino = arduino
        print("Initializing arduino with serial port " + self.serial_port)
        #self.arduino = serial.Serial(port='COM5', baudrate=57600, timeout=.1)
        print("Initializing servos...")
        self.bodyMotor = servo(self.arduino,0,560,2330,0,pi) #0 is left facing, pi is right facing
        self.shoulderMotor = servo(self.arduino,1,750,2200,0,8*pi/9) #0 is up, 8*pi/9 (160 degrees) is down
        self.elbowMotor = servo(self.arduino,2,550,1600,-5*pi/18,7*pi/36) # 1100 is 0 degrees, 550 is aboput -50 degrees, 2400 is the max value, but the servo cant handle higher than 1600 = 35 degrees.
        self.wristMotor = servo(self.arduino,3,550,2400,-0.22*pi,0.78*pi) #-22pi is close to the 0 positon at 950, then it rotates counter clockwise when moving to 0.78pi.
        self.gripperMotor = servo(self.arduino,4,550,2150,0,1) #0 is open, 1 is closed
        self.headMotor = servo(self.arduino,5,550,2340,0,pi) #0 is left, pi is right

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