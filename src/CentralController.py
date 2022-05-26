import numpy as np
from scipy import optimize
from sqlalchemy import true
import math

# c = [[3,8,6,9,5], [7,5,12,9,19], [7,10,9,10,6], [4,6,2,12,8], [9,9,6,15,11]]
# c = np.array(c)
# print(c)
# name_id,work_id=optimize.linear_sum_assignment(c)
# print(c[name_id,work_id ].sum())
# print(name_id,work_id)

class CentralController:
    def __init__(self,robotList,entranceList):
        self.robotList = robotList
        self.entranceList = entranceList
    def cost(self,robot,entrance):
        return math.sqrt((robot.x-entrance.x)**2+(robot.y-entrance.y)**2)
    def TargetPlanner(self,matrix,robot,entrance):
        name_id,work_id=optimize.linear_sum_assignment(matrix)
        num = len(robot)
        #print(name_id,work_id,num,len(entrance),len(robot))
        for i in range(num):
            self.robotList[robot[name_id[i]]].target = entrance[work_id[i]]+4
    def TargetPlanning(self):
        cnt_valid_robot = 0
        valid_robot_list = []
        for i in self.robotList:
            if i.target == -1 or (i.target>=4 and i.movingFlag==True):
                cnt_valid_robot+=1
                valid_robot_list.append(i.robotID)
        if cnt_valid_robot == 0:
            return
        cnt_require_entrance = 0
        cnt_require_entrance_urgent = 0
        entrance_normal = []
        entrance_urgent = []
        for i in self.entranceList:
            if len(i.Queue)==0:
                cnt_require_entrance_urgent += 1
                entrance_urgent.append(i.entranceID)
                cnt_require_entrance += 1
                entrance_normal.append(i.entranceID)
            elif len(i.Queue)==1:
                cnt_require_entrance += 1
                entrance_normal.append(i.entranceID)
        #after get the number of these, construct an sending problem
        #if urgent is more than valid robot
        if(cnt_valid_robot<=cnt_require_entrance_urgent):
            matrix = np.zeros(shape=(cnt_require_entrance_urgent,cnt_require_entrance_urgent))
            for i in range(len(valid_robot_list)):
                for j in range(len(entrance_urgent)):
                    matrix[i,j]=self.cost(self.robotList[valid_robot_list[i]],self.entranceList[entrance_urgent[j]])
            self.TargetPlanner(matrix,valid_robot_list,entrance_urgent)
        #if urgent is less than valid robot but urgent+normal is more than valid robot
        elif(cnt_valid_robot>cnt_require_entrance_urgent and cnt_valid_robot<=cnt_require_entrance+cnt_require_entrance_urgent):
            matrix = np.zeros(shape=(cnt_valid_robot,cnt_valid_robot))
            for i in range(cnt_valid_robot-cnt_require_entrance_urgent):
                entrance_urgent.append(entrance_normal[i])
            for i in range(len(valid_robot_list)):
                for j in range(len(entrance_urgent)):
                    matrix[i,j]=self.cost(self.robotList[valid_robot_list[i]],self.entranceList[entrance_urgent[j]])
            self.TargetPlanner(matrix,valid_robot_list,entrance_urgent)
            
        



