import numpy as np
import math


class AGVRobot:
    def __init__(self,x,y,target,robotID,movingFlag=False):
        self.x = x
        self.y = y
        self.target = target
        self.robotID = robotID
        self.v_magnitude = 15.0
        self.movingFlag = movingFlag
        self.helpSignal = 0
        self.Goals = [(25,12),(25,15),(25,18),(25,21)]
        self.Entrance = [(0,3),(0,12),(0,21),(0,30)]
    def init_pos(self):
        belong = self.robotID//2
        self.x = self.Entrance[belong][0]
        self.y = self.Entrance[belong][1]
    def getSpeedDir(self,robots):
        '''
        pertential field method or others,
        return (v_x,v_y)
        '''
        if self.movingFlag==False or self.target == -1:
            return (0,0)
        if self.target < len(self.Goals):
            v_x = self.Goals[self.target][0] - self.x
            v_y = self.Goals[self.target][1] - self.y
            norm = (v_x**2+v_y**2)**0.5
            v_x = v_x/(norm+0.01)
            v_y = v_y/(norm+0.01)
        else:
            v_x = self.Entrance[self.target-len(self.Goals)][0]-self.x
            v_y = self.Entrance[self.target-len(self.Goals)][1]-self.y
            norm = (v_x**2+v_y**2)**0.5
            v_x = v_x/(norm+0.01)
            v_y = v_y/(norm+0.01)
        self.v_magnitude = 25
        return (v_x*self.v_magnitude,v_y*self.v_magnitude)

    def ThrowLoad(self):
        curr_x = self.x
        curr_y = self.y
        if self.target < len(self.Goals):
            dst_x = self.Goals[self.target][0]
            dst_y = self.Goals[self.target][1]
            dist = math.sqrt((curr_x-dst_x)**2+(curr_y-dst_y)**2)
            if dist<0.5:
                self.target = -1
        # else:
        #     dst_x = self.Entrance[self.target-len(self.Goals)][0]
        #     dst_y = self.Entrance[self.target-len(self.Goals)][1]
        #     dist = math.sqrt((curr_x-dst_x)**2+(curr_y-dst_y)**2)