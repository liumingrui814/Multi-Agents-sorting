from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import colors
import numpy as np
from agvRobot import *
from inputHandler import *
from CentralController import *
import seaborn as sns
import random

class MAPFSimulator:
    def __init__(self, Robots,Entrances,Goals):
        self.robots = Robots
        self.entrances = Entrances
        self.goals = Goals
        self.CentralController = CentralController(self.robots,self.entrances)
        #initialize original queue of each Entrance
        for i in self.entrances:
            i.init_Queue()
            i.NewCommer()
        for i in self.robots:
            i.init_pos()

    def evolve(self, dt):
        timestep = 0.0001
        nsteps = int(dt / timestep)

        for i in range(nsteps):
            for e in self.entrances:
                if(len(e.Queue)>0):
                    if (e.commer>=0):
                        self.robots = e.SendoutAGV(self.robots)
                        e.commer = -1
                random.seed()
                rnd = random.randint(0,100000)
                if (rnd<=5 and e.commer==-1):
                    e.NewCommer()
                self.robots = e.RecieveAGV(self.robots)
            for p in self.robots:
                if p.movingFlag == True:
                    (v_x,v_y) = p.getSpeedDir(self.robots)
                    d_x = timestep * v_x
                    d_y = timestep * v_y
                    p.x += d_x
                    p.y += d_y
            for p in self.robots:
                p.ThrowLoad()
            self.CentralController.TargetPlanning()

    def visualize(self):
        X = [p.x for p in self.robots]
        Y = [p.y for p in self.robots]
        valueDict = {"start":4,"goal":5,"void":0,"obsticle":1,"rounte":2,"visit":3}
        cmap = colors.ListedColormap(['white','black','cyan','yellow','magenta','green'])
        colorlist = ['#FFA000', '#AF9500', '#5F5F50', '#00AF00', '#00ABA2','#FF00FF','#FF3022','#0230FF']
        shape = (40,40)
        #define magnitude of the figure
        fig = plt.figure(figsize=shape)
        #draw AGV Robots
        ax = plt.subplot(111, aspect = 'equal')
        plt.xlim(0, 40)
        plt.ylim(0, 40)
        line = ax.scatter([0], [0])

        #draw inputHandlers
        textHandler = []
        for i in self.entrances:
            ret = ax.text(0,0,'',fontdict={'size':'8','color':'k'})
            textHandler.append(ret)


        #draw grid map(Make sure you're confident before you change)
        field = np.zeros(shape)
        for i in self.entrances:
            field[i.y,i.x]=valueDict["start"]
        for i in self.goals:
            field[i[0],i[1]]=valueDict["goal"]
        ax = plt.gca() #get current axes
        sns.heatmap(field,cmap=cmap,vmin=0,vmax=5,linewidths=0.3,
                    linecolor= 'gray',ax=ax,cbar=False)
        ax.xaxis.tick_top()#label is in the top of the figure
        ax.xaxis.set_label_position("top")
        #ax.set_ylabel("rows") #verticle way is rows(y)#ax.set_xlabel("cols") #horizontal way is cols(x)
        #number noted among axes
        ax.set_xticks(np.arange(shape[1]))
        ax.set_yticks(np.arange(shape[0])) #mark of the axis
        labels = ax.set_xticklabels([str(i) for i in range(shape[1])],fontsize = 3) 
        labels = ax.set_yticklabels([str(i) for i in range(shape[0])],fontsize = 3) 
        ax.set_aspect(1.0)#height is equal to width

        def init():
            line.set_offsets((0, 0)) 
            for i in range(len(textHandler)):
                textHandler[i].set_position((30+i,0))
                textHandler[i].set_text('')
            #line.set_data(X, Y)
            return tuple(textHandler+[line])

        def animate(aa):
            self.evolve(0.01)
            colr = []
            X = []
            Y = []
            pos = []
            for i in self.robots:
                if i.movingFlag == True:
                    X.append(i.x)
                    Y.append(i.y)
                    pos.append((i.x,i.y))
                    colr.append(colorlist[i.robotID])
            #X = [p.x for p in self.robots]
            #Y = [p.y for p in self.robots]
            for i in range(len(textHandler)):
                textHandler[i].set_position((0,i*1.5+34))
                textHandler[i].set_text('En%d:%d'%(i,len(self.entrances[i].Queue)))
            line.set_offsets(pos)
            line.set_color(c=colr)
            return tuple(textHandler+[line])

        anim = animation.FuncAnimation(fig,
                                    animate,
                                    frames=10,
                                    init_func = init,
                                    blit = True,
                                    interval = 10)
        plt.show()       

if __name__ == '__main__':
    particles = [AGVRobot(10, 5, 1,0),
                 AGVRobot(0, 15, -1,1),
                 AGVRobot(13, 12, 3,2),
                 AGVRobot(0, 0, 0,3),
                 AGVRobot(0, 0, 0,4),
                 AGVRobot(0, 0, 0,5),
                 AGVRobot(0, 0, 0,6),
                 AGVRobot(0, 0, 0,7),]
    Entrances = [Entrance(0,3,'normal',0),
                 Entrance(0,12,'normal',1),
                 Entrance(0,21,'normal',2),
                 Entrance(0,30,'normal',3)]
    Goals = [(12,25),(15,25),(18,25),(21,25)]
    simulator = MAPFSimulator(particles,Entrances,Goals)
    simulator.visualize()