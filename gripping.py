import numpy as np
from math import *
from gekko import GEKKO
from Robot_Control.robotControl import robot

class grip(robot):
   
   def __init__(self, hubert, verbose, debug):
      self.m = GEKKO()
      self.verbose = verbose
      self.debug = debug
      # self.vector_length = vector_length #not in use atm
      # self.verbose = verbose
      # self.debug = debug

      self.posArm = np.zeros(3)
      self.angle = np.zeros(3)
      self.vectorDir = np.zeros(2)

      self.hubert = hubert

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
      x = sm.Var(value=self.posArm[0])
      y = sm.Var(value=self.posArm[1])
      z = sm.Var(0.1325)

      # lower bounds
      x.LOWER = self.posArm[0]-self.error
      y.LOWER = self.posArm[1]-self.error
      z.LOWER = 0.135

      # upper bounds
      x.UPPER = self.posArm[0]+self.error
      y.UPPER = self.posArm[1]+self.error
      z.UPPER = 0.14
      
       # equation 
      sm.Equations([
         ((0.204*sm.sin(theta__3) + 0.015)*sm.cos(theta__2) + (0.204*sm.cos(theta__3) + 0.088)*sm.sin(theta__2) + 0.034)*sm.cos(theta__1) + 0.103*sm.sin(theta__1) - x==0, 
         ((0.204*sm.sin(theta__3) + 0.015)*sm.cos(theta__2) + (0.204*sm.cos(theta__3) + 0.088)*sm.sin(theta__2) + 0.034)*sm.sin(theta__1) - 0.103*sm.cos(theta__1) - y==0,
         (-0.204*sm.cos(theta__3) - 0.088)*sm.cos(theta__2) + (0.204*sm.sin(theta__3) + 0.015)*sm.sin(theta__2) + 0.360 - z==0
         ]) 

      try:
         sm.solve(disp=False)
      except:
         return -1
         # solve
      # print([theta__1.value[0],theta__2.value[0],theta__3.value[0]]) # print solution
      self.hubert.move('body',theta__1.value[0])
      self.hubert.move('shoulder',theta__2.value[0])
      self.hubert.move('elbow',theta__3.value[0])
      self.hubert.move("gripper", 0.9)

   def __kinematic(self):
      theta__1 = self.hubert.get_angle('body')
      theta__2 = self.hubert.get_angle('shoulder')
      theta__3 = self.hubert.get_angle('elbow')
      
      if (self.debug):
        print("Printing body angles...")
        print("Body angle: " + str(theta__1) + "\nShoulder angle: " + str(theta__2) + "\nElbow angle: " + str(theta__3))

      self.posArm[0] = ((0.204*sin(theta__3) + 0.015)*cos(theta__2) + (0.204*cos(theta__3) + 0.088)*sin(theta__2) + 0.034)*cos(theta__1) + 0.103*sin(theta__1)
      self.posArm[1] = ((0.204*sin(theta__3) + 0.015)*cos(theta__2) + (0.204*cos(theta__3) + 0.088)*sin(theta__2) + 0.034)*sin(theta__1) - 0.103*cos(theta__1)
      self.posArm[2] = (-0.204*cos(theta__3) - 0.088)*cos(theta__2) + (0.204*sin(theta__3) + 0.015)*sin(theta__2) + 0.360


      self.angle[0] = theta__1 
      self.angle[1] = theta__2 
      self.angle[2] = theta__3 

   # hand position, shape position 
   def motion(self, error):
      self.m.clear()
      self.error = error
      #self.angle = angle # in the final code will be taken from the robot class

      # extract the value from the object robot 
      self.__kinematic()

      # calculate numerically the new position of the arm
      if self.__function() == -1:
         return -1






