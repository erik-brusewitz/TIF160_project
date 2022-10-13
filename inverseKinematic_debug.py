import numpy as np
from math import *
from gekko import GEKKO
from Robot_Control.robotControl import robot




class direction():

   def __init__(self):
      self.m = GEKKO()

      self.posArm = np.zeros(3)
      self.angle = np.zeros(3)
      self.vectorDir = np.zeros(2)

      # self.hubert = hubert

   def __vector(self,head):
      self.vectorDir[0] = self.camera_posShape[0] - self.camera_posArm[0] 
      self.vectorDir[1] = self.camera_posShape[1] - self.camera_posArm[1]
      # the vector has to be rotated in the absolute reference frame because now is expressed in the camera reference frame 
      # head_angle = head
      # body_angle = self.angle[0]
      # theta = head_angle + body_angle
      # c, s = np.cos(theta), np.sin(theta)
      # R = np.array(((c, -s), (s, c)))
      # vectorDir = R.dot(vectorDir)
      # normalization of the vector and step of 2 cm
      self.vectorDir = self.vectorDir/np.linalg.norm(self.vectorDir) * 0.01
      
   def __function(self):#,z):
      sm = self.m

      theta__1 = sm.Var(value=self.angle[0] )      
      theta__2 = sm.Var(value=self.angle[1] )      
      theta__3 = sm.Var(value=self.angle[2] ) 

      # lower bounds
      theta__1.LOWER = 0
      theta__2.LOWER = 0
      theta__3.LOWER = -pi/2

      # upper bounds
      theta__1.UPPER = pi
      theta__2.UPPER = pi
      theta__3.UPPER = pi/2

      # Variables
      x = sm.Var(value=0)
      y = sm.Var(value=0.21)
      z = 0.135

      # lower bounds
      x.LOWER = -0.01
      y.LOWER = 0.21-0.01


      # upper bounds
      x.UPPER = 0+0.005
      y.UPPER = 0.21+0.02
      
      # x = (self.posArm[0] + self.vectorDir[0])
      # y = (self.posArm[1] + self.vectorDir[1])
      # z = (self.posArm[2])
      # x = 0
      # y = 0.21
      # z = 0.135
      
      
       # equation 
      sm.Equations([
         ((0.204*sm.sin(theta__3) + 0.015)*sm.cos(theta__2) + (0.204*sm.cos(theta__3) + 0.088)*sm.sin(theta__2) + 0.034)*sm.cos(theta__1) + 0.103*sm.sin(theta__1) - x==0, 
         ((0.204*sm.sin(theta__3) + 0.015)*sm.cos(theta__2) + (0.204*sm.cos(theta__3) + 0.088)*sm.sin(theta__2) + 0.034)*sm.sin(theta__1) - 0.103*sm.cos(theta__1) - y==0,
         (-0.204*sm.cos(theta__3) - 0.088)*sm.cos(theta__2) + (0.204*sm.sin(theta__3) + 0.015)*sm.sin(theta__2) + 0.360 - z==0
      ]) 

      # m.options.MAX_ITER = 20
      # m.options.OTOL = 1.0e-3
      while True:
         try: 
            sm.solve(disp=False)     # solve
            break
         except:
            print("Except cought")
            y += 0.005
            sm.Equations([
               ((0.204*sm.sin(theta__3) + 0.015)*sm.cos(theta__2) + (0.204*sm.cos(theta__3) + 0.088)*sm.sin(theta__2) + 0.034)*sm.cos(theta__1) + 0.103*sm.sin(theta__1) - x==0, 
               ((0.204*sm.sin(theta__3) + 0.015)*sm.cos(theta__2) + (0.204*sm.cos(theta__3) + 0.088)*sm.sin(theta__2) + 0.034)*sm.sin(theta__1) - 0.103*sm.cos(theta__1) - y==0,
               (-0.204*sm.cos(theta__3) - 0.088)*sm.cos(theta__2) + (0.204*sm.sin(theta__3) + 0.015)*sm.sin(theta__2) + 0.360 - z==0
            ]) 


      print([theta__1.value[0],theta__2.value[0],theta__3.value[0]]) # print solution 
      print([x.value[0],y.value[0]]) # print solution
      return  [theta__1.value[0],theta__2.value[0],theta__3.value[0]]

   def __kinematic(self,theta__1,theta__2,theta__3):
      # theta__1 = self.hubert.angle('body')
      # theta__2 = self.hubert.sholder('shoulder')
      # theta__3 = self.hubert.elbow('elbow')


      # self.posArm[0] = ((-0.204*sin(elbow) + 0.015)*cos(shoulder) + (-0.204*cos(elbow) - 0.088)*sin(shoulder) + 0.034)*cos(body) + 0.103*sin(body) - (self.posArm[0] + self.delta * self.vectorDir[0])
      # self.posArm[1] = ((-0.204*sin(elbow) + 0.015)*cos(shoulder) + (-0.204*cos(elbow) - 0.088)*sin(shoulder) + 0.034)*sin(body) - 0.103*cos(body) - (self.posArm[1] + self.delta * self.vectorDir[1])
      # self.posArm[2] = (-0.204*cos(elbow) - 0.088)*cos(shoulder)+ (0.204*sin(elbow) - 0.015)*sin(shoulder) + 0.360 - (self.posArm[2] + self.delta * self.vectorDir[2])
      self.posArm[0] = ((0.204*sin(theta__3) + 0.015)*cos(theta__2) + (0.204*cos(theta__3) + 0.088)*sin(theta__2) + 0.034)*cos(theta__1) + 0.103*sin(theta__1)
      self.posArm[1] = ((0.204*sin(theta__3) + 0.015)*cos(theta__2) + (0.204*cos(theta__3) + 0.088)*sin(theta__2) + 0.034)*sin(theta__1) - 0.103*cos(theta__1)
      self.posArm[2] = (-0.204*cos(theta__3) - 0.088)*cos(theta__2) + (0.204*sin(theta__3) + 0.015)*sin(theta__2) + 0.360


      self.angle[0] = theta__1 
      self.angle[1] = theta__2 
      self.angle[2] = theta__3 

   def motion(self, theta__1,theta__2,theta__3, arm, shape):
      self.camera_posArm = arm 
      self.camera_posShape = shape
      #self.angle = angle # in the final code will be taken from the robot class
      
      # extract the value from the object robot 
      self.__kinematic(theta__1,theta__2,theta__3)

      # direction vector to the shape
      self.__vector(0)

      # calculate numerically the new position of the arm
      return self.__function()
      

direc = direction()

direc.motion(1.57, 0.1, 0.175, [0.8,0.47], [0.36, 0.64])




