import numpy as np
from math import *
from gekko import GEKKO
from Robot_Control.robotControl import robot

class direction(robot):
   
   def __init__(self, hubert, vector_length, verbose, debug):
      self.m = GEKKO()
      self.step = 0.03
      self.vector_length = vector_length #not in use atm
      self.verbose = verbose
      self.debug = debug

      self.posArm = np.zeros(3)
      self.angle = np.zeros(3)
      self.vectorDir = np.zeros(2)

      self.hubert = hubert

   def __vector(self):
      self.vectorDir[0] = self.camera_posShape[0] - self.camera_posArm[0] 
      self.vectorDir[1] = self.camera_posShape[1] - self.camera_posArm[1]
      # the vector has to be rotated in the absolute reference frame because now is expressed in the camera reference frame 
      # head_angle = self.hubert.get_angle('head')
      # body_angle = self.hubert.get_angle('body')
      # theta = body_angle # + head angle in case we move it 
      # c, s = np.cos(theta), np.sin(theta)
      # R = np.array(((c, -s), (s, c)))
      # self.vectorDir = R.dot(self.vectorDir)
      # normalization of the vector and step of 2 cm
      self.vectorDir = self.vectorDir/np.linalg.norm(self.vectorDir) * self.step
      
      if self.debug:
         print("Directional vector = (" + str(self.vectorDir[0]) + ", " + str(self.vectorDir[1]) + ")")

   def __function(self):#,z):
      sm = self.m

      theta__1 = sm.Var(value=self.angle[0] )      
      theta__2 = sm.Var(value=self.angle[1] )      
      theta__3 = sm.Var(value=self.angle[2] ) 
      
      # lower bounds
      theta__1.LOWER = 0
      theta__2.LOWER = 0
      theta__3.LOWER = -50*pi/180

      # upper bounds
      theta__1.UPPER = pi
      theta__2.UPPER = pi
      theta__3.UPPER = 35*pi/180

      # Variables
      x = sm.Var(value=self.posArm[0] + self.vectorDir[0])
      y = sm.Var(value=self.posArm[1] + self.vectorDir[1])
      z = sm.Var(value=0.14)

      # lower bounds
      x.LOWER = self.posArm[0] + self.vectorDir[0]-self.error
      y.LOWER = self.posArm[1] + self.vectorDir[1]-self.error
      z.LOWER = 0.14

      # upper bounds
      x.UPPER = self.posArm[0] + self.vectorDir[0]+self.error
      y.UPPER = self.posArm[1] + self.vectorDir[1]+self.error
      z.UPPER = 0.16
      
       # equation 
      sm.Equations([
         ((0.204*sm.sin(theta__3) + 0.015)*sm.cos(theta__2) + (0.204*sm.cos(theta__3) + 0.088)*sm.sin(theta__2) + 0.034)*sm.cos(theta__1) + 0.103*sm.sin(theta__1) - x==0, 
         ((0.204*sm.sin(theta__3) + 0.015)*sm.cos(theta__2) + (0.204*sm.cos(theta__3) + 0.088)*sm.sin(theta__2) + 0.034)*sm.sin(theta__1) - 0.103*sm.cos(theta__1) - y==0,
         (-0.204*sm.cos(theta__3) - 0.088)*sm.cos(theta__2) + (0.204*sm.sin(theta__3) + 0.015)*sm.sin(theta__2) + 0.360 - z==0
         ]) 

      # m.options.MAX_ITER = 20
      # m.options.OTOL = 1.0e-3
      try:
         sm.solve(disp=False)
      except:
         return -1
         # solve
      # print([theta__1.value[0],theta__2.value[0],theta__3.value[0]]) # print solution
      self.hubert.move('body',theta__1.value[0])
      self.hubert.move('shoulder',theta__2.value[0])
      self.hubert.move('elbow',theta__3.value[0])

   def __kinematic(self):
      theta__1 = self.hubert.get_angle('body')
      theta__2 = self.hubert.get_angle('shoulder')
      theta__3 = self.hubert.get_angle('elbow')
      
      if self.debug:
         print("Printing body angles...")
         print("Body angle: " + str(theta__1) + "\nShoulder angle: " + str(theta__2) + "\nElbow angle: " + str(theta__3))

      self.posArm[0] = ((0.204*sin(theta__3) + 0.015)*cos(theta__2) + (0.204*cos(theta__3) + 0.088)*sin(theta__2) + 0.034)*cos(theta__1) + 0.103*sin(theta__1)
      self.posArm[1] = ((0.204*sin(theta__3) + 0.015)*cos(theta__2) + (0.204*cos(theta__3) + 0.088)*sin(theta__2) + 0.034)*sin(theta__1) - 0.103*cos(theta__1)
      self.posArm[2] = (-0.204*cos(theta__3) - 0.088)*cos(theta__2) + (0.204*sin(theta__3) + 0.015)*sin(theta__2) + 0.360

      if (self.verbose):
         print("########")  
         print("New body angle = " + str(theta__1) + "\nNew shoulder angle = " + str(theta__2) + "\nNew elbow angle = " + str(theta__3) + "/n")
         print("########")
      self.angle[0] = theta__1 
      self.angle[1] = theta__2 
      self.angle[2] = theta__3 

   # hand position, shape position 
   def motion(self, arm, shape, error):
      self.m.clear()
      self.error = error
      self.camera_posArm = arm 
      self.camera_posShape = shape
      self.camera_posArm[1] = 1 - self.camera_posArm[1]
      self.camera_posShape[1] = 1 - self.camera_posShape[1]
      #self.angle = angle # in the final code will be taken from the robot class
      
      # direction vector to the shape
      self.__vector()

      # extract the value from the object robot 
      self.__kinematic()

      # calculate numerically the new position of the arm
      if self.__function() == -1:
         return -1






