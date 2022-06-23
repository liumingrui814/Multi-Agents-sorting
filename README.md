## Multi-Agents in sorting and path plannnig
> lmrlmrlmrlmr2022/5/21

### 简单说明

- `agvRobot.py`: 定义小车的类，暂时先加了位置，ID，目的地等信息

  - 里面有计算小车速度的函数`getSpeedDir`,不知道用栅格的话需不需要修改，在连续空间里算出速度就够了，函数中小车`movingFlag=0,target=1`均不会计算速度，此时小车停。
  - `movingFlag`: 1小车可移动，0小车在排队
  - `target`:  0\~3对应4个目标，4\~7对应四个入口（入口编号+目标编号）
  - `ThrowLoad`: 判断小车有没有到丢东西的地方，丢了东西之后target置-1，

- `inputHandler.py`:定义货物入口的类，暂时先加了位置，排队状态`state`，ID等信息

- `simulator.py`:实时仿真的类，里面有画栅格地图和画小车的代码

  - `evolve`是实时更新的代码，目前里面只放了小车的位置变化，小车丢东西检测、入口派出、入口接收、小车返回实时目标规划（二分图指派问题）根据小车的速度推算了小车的位置，后续需要在evolve里进行各式各样的更新操作。

  - `visualize`是画图的代码，用了matplotlib的animate, 目前动态的只有小车和入口对列，如果有其他可视化需求需要后续修改

    ```python
    valueDict = {"start":4,"goal":5,"void":0,"obsticle":1,"rounte":2,"visit":3}
    cmap = colors.ListedColormap(['white','black','cyan','yellow','magenta','green'])
    ```

是给栅格赋颜色的，字典里的值对应格子，暂定有空、目标、起始位置、障碍、路线。cmap里给对应的值赋颜色

- 除了evolve和animate(如果有想要的其他的动态更新的要去animate里加一下，就把plt这些的返回值返回就行), 返回的指派和连续空间的速度变化都不需要修改animate


### 坐标系：

- 左上角（0，0），右上角（40，0），左下角（0，40）
- 对于栅格的绘制，则是按**矩阵顺序**（左下角（40，0）），如需要添加其他栅格的颜色或可视化则需要特别注意在（x,y)里算出来的坐标要画到栅格上时（x,y)要换成（y,x）。
