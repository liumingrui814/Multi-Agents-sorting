import numpy as np
import math
import random
from agvRobot import *
class Entrance:
    def __init__(self,x,y,state='normal', entranceID=0):
        self.x = x
        self.y = y
        self.state = state
        self.entranceID = entranceID
        self.Queue = []
        self.commer = 0
    def init_Queue(self):
        """
        two AGVRobots are waiting in the initial condition 
        """
        self.Queue.append(self.entranceID*2)
        self.Queue.append(self.entranceID*2+1)
    def NewCommer(self):
        random.seed()
        self.commer =  random.randint(0,3)
    def SendoutAGV(self,robotList):
        # update queue
        if(len(self.Queue)>0):
            outrobotID = self.Queue[0]
            robotList[outrobotID].target = self.commer
            robotList[outrobotID].movingFlag = True
            self.Queue.pop(0)
        return robotList
    def RecieveAGV(self,robotList):
        # update queue
        # print(robotList[0].target)
        for i in robotList:
            curr_x = i.x
            curr_y = i.y
            dst_x = self.x
            dst_y = self.y
            dist = math.sqrt((curr_x-dst_x)**2+(curr_y-dst_y)**2)
            if dist<0.5 and i.target>=4 and i.movingFlag==True: 
                self.Queue.append(i.robotID)
                i.movingFlag=False
        return robotList
    def CallForAGV(self,robotList):
        for i in robotList:
            i.helpSignal = self.entranceID

        
        
