import numpy as np
from math import *
from scipy.optimize import differential_evolution
from gekko import GEKKO
from Robot_Control.robotControl import robot

# global x, y, z

# x = 0.049
# y = -0.103
# z = 0.068

# def myFunction(z):
#    theta1 = z[0]
#    theta2 = z[1]
#    theta3 = z[2]

#    F = np.empty((3))
#    F[0] = ((-0.204*sin(theta3) + 0.015)*cos(theta2) + (-0.204*cos(theta3) - 0.088)*sin(theta2) + 0.034)*cos(theta1) + 0.103*sin(theta1) - 0.049
#    F[1] = ((-0.204*sin(theta3) + 0.015)*cos(theta2) + (-0.204*cos(theta3) - 0.088)*sin(theta2) + 0.034)*sin(theta1) - 0.103*cos(theta1) + 0.103
#    F[2] = (-0.204*cos(theta3) - 0.088)*cos(theta2)+ (0.204*sin(theta3) - 0.015)*sin(theta2) + 0.360 - 0.068
#    a=3
#    return F

# zGuess = np.array([0.1,0.11,0])
# z = fsolve(myFunction,zGuess)
# print(z)


class motion:
   def __init__(self, posArm, posShape, angle):
      self.posArm = posArm 
      self.posShape = posShape
      self.angle = angle
      self.__vector()

   def __vector(self):
      self.vectorDir = np.zeros(3)
      self.vectorDir[0] = self.posShape[0] - self.posArm[0] 
      self.vectorDir[1] = self.posShape[1] - self.posArm[1]
      self.vectorDir[2] = self.posShape[2] - self.posArm[2]

   def __function(self):#,z):
      # theta1 = z[0]
      # theta2 = z[1]
      # theta3 = z[2]
      # f = np.array([(self.posArm[0] + self.delta * self.vectorDir[0]),(self.posArm[1] + self.delta * self.vectorDir[1]),(self.posArm[2] + self.delta * self.vectorDir[2])])
      # print(f)
      # F = np.empty((3))
      # F[0] = ((-0.204*sin(theta3) + 0.015)*cos(theta2) + (-0.204*cos(theta3) - 0.088)*sin(theta2) + 0.034)*cos(theta1) + 0.103*sin(theta1) - (self.posArm[0] + self.delta * self.vectorDir[0])
      # F[1] = ((-0.204*sin(theta3) + 0.015)*cos(theta2) + (-0.204*cos(theta3) - 0.088)*sin(theta2) + 0.034)*sin(theta1) - 0.103*cos(theta1) - (self.posArm[1] + self.delta * self.vectorDir[1])
      # F[2] = (-0.204*cos(theta3) - 0.088)*cos(theta2)+ (0.204*sin(theta3) - 0.015)*sin(theta2) + 0.360 - (self.posArm[2] + self.delta * self.vectorDir[2])
      # return F

      # print([((-0.204*sin(theta3) + 0.015)*cos(theta2) + (-0.204*cos(theta3) - 0.088)*sin(theta2) + 0.034)*cos(theta1) + 0.103*sin(theta1) - (self.posArm[0] + self.delta * self.vectorDir[0]),((-0.204*sin(theta3) + 0.015)*cos(theta2) + (-0.204*cos(theta3) - 0.088)*sin(theta2) + 0.034)*sin(theta1) - 0.103*cos(theta1) - (self.posArm[1] + self.delta * self.vectorDir[1]),(-0.204*cos(theta3) - 0.088)*cos(theta2)+ (0.204*sin(theta3) - 0.015)*sin(theta2) + 0.360 - (self.posArm[2] + self.delta * self.vectorDir[2])])

      m = GEKKO()             # create GEKKO model
      
      theta1 = m.Var(value=self.angle[0] )      
      theta2 = m.Var(value=self.angle[1] )      
      theta3 = m.Var(value=self.angle[2] ) 

      #lower bounds
      theta1.LOWER = 0
      theta2.LOWER = -pi
      theta3.LOWER = -pi/2

      #upper bounds
      theta1.UPPER = pi
      theta2.UPPER = 0
      theta3.UPPER = 0

      x = (self.posArm[0] + self.delta * self.vectorDir[0])
      y = (self.posArm[1] + self.delta * self.vectorDir[1])
      z = (self.posArm[2] + self.delta * self.vectorDir[2])
      
      m.Equations([
         ((-0.204*m.sin(theta3) + 0.015)*m.cos(theta2) + (-0.204*m.cos(theta3) - 0.088)*m.sin(theta2) + 0.034)*m.cos(theta1) + 0.103*m.sin(theta1) - x==0, 
         ((-0.204*m.sin(theta3) + 0.015)*m.cos(theta2) + (-0.204*m.cos(theta3) - 0.088)*m.sin(theta2) + 0.034)*m.sin(theta1) - 0.103*m.cos(theta1) - y==0,
         (-0.204*m.cos(theta3) - 0.088)*m.cos(theta2) + (0.204*m.sin(theta3) - 0.015)*m.sin(theta2) + 0.360 - z==0
         ])  

      m.options.MAX_ITER = 20
      m.options.OTOL = 1.0e-3
      m.solve(disp=False)     # solve
      print([theta1.value[0],theta2.value[0],theta3.value[0]]) # print solution   

   

   def trajectory(self, step):
      self.delta = 1 / step
      angleOut = np.zeros((step,3))
      for i in range(step):
         angleGuess = self.angle
         # boundsC = [(0,pi),(-pi,0),(-pi/2,0)] # bounds 
         # z = differential_evolution(self.__function,angleGuess,bounds=boundsC)
         self.__function()
         #self.angle = z
         #angleOut[i] = z
         self.delta += self.delta
         #print(z)
      return angleOut

a = np.array([0.3215447912, -0.103, 0.3207761292])
b = np.array([0.3083204199, -0.103, 0.2764685742])
c = np.array([0,-pi/3,-pi/6])
mot = motion(a,b,c)
# f = mot.trajectory(1)
z = mot.trajectory(1)
print(z)



def direction(robot):
   vectorDir = np.zeros(2)
   def __init__(self):
      self.m = GEKKO()

      # lower bounds
      self.theta1.LOWER = 0
      self.theta2.LOWER = -pi
      self.theta3.LOWER = -pi/2

      # upper bounds
      self.theta1.UPPER = pi
      self.theta2.UPPER = 0
      self.theta3.UPPER = 0

      self.posArm = np.zeros(3)
      self.angle = np.zeros(3)


   def motion(self, arm, shape):
      self.camera_posArm = arm 
      self.camera_posShape = shape
      #self.angle = angle # in the final code will be taken from the robot class
      
      # direction vector to the shape
      self.__vector()

      # extract the value from the object robot 
      self.__kinematic()

      # calculate numerically the new position of the arm
      self.__function()

   def __vector(self):
      vectorDir[0] = self.camera_posShape[0] - self.camera_posArm[0] 
      vectorDir[1] = self.camera_posShape[1] - self.camera_posArm[1]
      # the vector has to be rotated in the absolute reference frame because now is expressed in the camera reference frame 
      head_angle = robot.angle('head')
      body_angle = robot.angle('body')
      theta = head_angle + body_angle
      c, s = np.cos(theta), np.sin(theta)
      R = np.array(((c, -s), (s, c)))
      vectorDir = R.dot(vectorDir)
      # normalization of the vector and step of 2 cm
      vectorDir = vectorDir/np.linalg.norm(vectorDir) * 0.02
      
   def __function(self):#,z):
      sm = self.m

      

      theta1 = sm.Var(value=self.angle[0] )      
      theta2 = sm.Var(value=self.angle[1] )      
      theta3 = sm.Var(value=self.angle[2] ) 


      x = (self.posArm[0] + self.vectorDir[0])
      y = (self.posArm[1] + self.vectorDir[1])
      z = (self.posArm[2])
      
       # equation 
      sm.Equations([
         ((-0.204*sm.sin(theta3) + 0.015)*sm.cos(theta2) + (-0.204*sm.cos(theta3) - 0.088)*sm.sin(theta2) + 0.034)*sm.cos(theta1) + 0.103*sm.sin(theta1) - x==0, 
         ((-0.204*sm.sin(theta3) + 0.015)*sm.cos(theta2) + (-0.204*sm.cos(theta3) - 0.088)*sm.sin(theta2) + 0.034)*sm.sin(theta1) - 0.103*sm.cos(theta1) - y==0,
         (-0.204*sm.cos(theta3) - 0.088)*sm.cos(theta2) + (0.204*sm.sin(theta3) - 0.015)*sm.sin(theta2) + 0.360 - z==0
         ]) 

      # m.options.MAX_ITER = 20
      # m.options.OTOL = 1.0e-3
      sm.solve(disp=False)     # solve
      print([theta1.value[0],theta2.value[0],theta3.value[0]]) # print solution  

   def __kinematic(self):
      body = robot.angle('body')
      shoulder = robot.sholder('shoulder')
      elbow = robot.elbow('elbow')


      self.posArm[0] = ((-0.204*sin(elbow) + 0.015)*cos(shoulder) + (-0.204*cos(elbow) - 0.088)*sin(shoulder) + 0.034)*cos(body) + 0.103*sin(body) - (self.posArm[0] + self.delta * self.vectorDir[0])
      self.posArm[1] = ((-0.204*sin(elbow) + 0.015)*cos(shoulder) + (-0.204*cos(elbow) - 0.088)*sin(shoulder) + 0.034)*sin(body) - 0.103*cos(body) - (self.posArm[1] + self.delta * self.vectorDir[1])
      self.posArm[2] = (-0.204*cos(elbow) - 0.088)*cos(shoulder)+ (0.204*sin(elbow) - 0.015)*sin(shoulder) + 0.360 - (self.posArm[2] + self.delta * self.vectorDir[2])

      self.angle[0] = body 
      self.angle[1] = shoulder 
      self.angle[2] = elbow 




