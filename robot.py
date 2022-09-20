from math import pi
import time
import serialCommunication as sc

# class that is used to control the servo motor of the robot,
# it has different function:
# - .info() to get the information about the servo 
# - .move( angle ) move the servo to that specific angle
class servo:
    def __init__(self, servo_id, minPosition, maxPosition, range):
        self.servo_id = servo_id
        self.minPosition = minPosition
        self.maxPosition = maxPosition
        self.range = range
        self.move(0)

    def info(self):
        print("servo_id:", self.servo_id, "angle: ", self.angle, "position: ", self.position, " minPosition:", self.minPosition, "maxPosition: ", self.maxPosition)

    def move(self, newAngle):
        print('Start the communication to move servo')
        self.position = int(self.minPosition + (newAngle / self.range) * ( self.maxPosition - self.minPosition))
        position_string = str(self.position)
        if self.position < 550 or self.position > 2400:
            print("Error, position is too large or too low")
        if self.position < 1000:
            sc.send_package(str(self.servo_id) + "0" + str(self.position))
        else:
            sc.send_package(str(self.servo_id) + str(self.position))
        print('End the communication to move servo')
        self.angle = newAngle
            
        return 0

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
    def __init__(self):
        self.bodyMotor = servo(0,560,2330,pi)
        self.shoulderMotor = servo(1,750,2200,pi)
        self.elbowMotor = servo(2,550,2400,pi)
        self.wristMotor = servo(3,950,2400,pi)
        self.gripperMotor = servo(4,550,2150,pi)
        self.headMotor = servo(5,550,2340,pi)

    def __motorC(self, motor):
        if ( motor == 'head'):
            r = self.headMotor
        elif ( motor == 'shoulder'):
            r = self.shoulderMotor
        elif ( motor == 'elbow'):
            r = self.shoulderMotor
        elif ( motor == 'wrist'):
            r = self.shoulderMotor
        elif ( motor == 'gripper'):
            r = self.shoulderMotor
        elif ( motor == 'head'):
            r = self.shoulderMotor
        else: 
            r = 1
        return r


    def move(self, motor, angle):
        r = self.__motorC(motor)
        
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