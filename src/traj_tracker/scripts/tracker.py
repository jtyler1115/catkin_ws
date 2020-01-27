#!/usr/bin/env python

import rospy
import numpy as np
import math
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import turtlesim.srv
import time
import matplotlib.pyplot as plt
global currentPos
currentPos = Pose()
def callback(data):
    #print(data)
    global currentPos
    currentPos = data
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def listener():
    rospy.init_node("tracker",anonymous=True)
    pub = rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=10)
    rospy.Subscriber("/turtle1/pose",Pose,callback)
    trajectory = rospy.get_param('trajectory_description')
    rate = rospy.Rate(2.66)
    
    xdlist=trajectory['list_of_x']
    ydlist=trajectory['list_of_y']
    dt=trajectory['timestep']
    controlMsg = Twist()
    global currentPos
    #print currentPos
    k1 = 1
    k2 = 1
    k3 = .2
    #randMsg.linear = [random.randint(1,10),random.randint(1,10),random.randint(1,10)]
    #randMsg.angular = [random.randint(1,10),random.randint(1,10),random.randint(1,10)]
    iteration = 0
    segments = 4
    index = 0

    vel=[0,0]
    acc=[0,0]

    #starting position
    xdold = 0
    ydold = 0
    xd = xdlist [0]
    yd = ydlist[0]
    eMat = np.array([[0],[0],[0]])
    kill=rospy.ServiceProxy('kill', turtlesim.srv.Kill)
    kill('turtle1')
    spawn=rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    spawn(0,10,1.5,'turtle1')
    setpen=rospy.ServiceProxy('turtle1/set_pen', turtlesim.srv.SetPen)
    #setpen(128,127,128,1,0)
    time.sleep(2)
    loop=-1
    t=0
    tout=[]
    xout=[]
    yout=[]
    thetaout=[]
    while not rospy.is_shutdown():
        
        index = (iteration % (4*segments))/segments
            #print(index)
        
        if iteration % segments == 0:
            xd = xdlist[index]
            yd = ydlist[index]
            loop += 1
        else:
            xd = xdold + float(xdlist[(index+1)%4]-xdlist[index])/float(segments)
            yd = ydold + float(ydlist[(index+1)%4]-ydlist[index])/float(segments)
        #xd = xdlist[index]
        #yd = ydlist[index]
        '''if (abs(xd - currentPos.x) < .1) and (abs(yd - currentPos.y) < .1):
            index +=1
            index = index % 4
            xd = xdlist[index]
            yd = ydlist[index]'''

        deltax = xd-currentPos.x
        deltay = yd-currentPos.y
        if (deltax != 0):
            thetad = math.atan2(deltay,deltax)
        else:
            thetad = 0

        vel[0] = deltax/dt
        vel[1] = deltay/dt

        acc[0] = (vel[0]-currentPos.linear_velocity*math.cos(currentPos.theta))/dt
        acc[1] = (vel[1]-currentPos.linear_velocity*math.sin(currentPos.theta))/dt


        rotMat=np.array([[math.cos(currentPos.theta),math.sin(currentPos.theta),0],[-math.sin(currentPos.theta),math.cos(currentPos.theta),0],[0,0,1]])
        
        diffMat=np.array([[xd-currentPos.x],[yd-currentPos.y],[thetad-currentPos.theta]])
        eMat=np.matmul(rotMat,diffMat)

        ud = math.sqrt((vel[0])**2 + (vel[1])**2)
        if (ud != 0):
            wd = (acc[1]*vel[0] - vel[1]*acc[0])/(vel[0]**2 + vel[1]**2)
        else:
            wd = 0
        u1 = -k1 * eMat[0,0]
        u2 = -k2 * eMat[1,0] -k3 * eMat[2,0]
        u = ud * math.cos(eMat[2,0]) - u1
        u = .5 * u
        #working tuning: scale u to 75% of original value
        # k = [1,1,.5]
        w = wd - u2
        print("xd: " + str(xd))
        print("yd: " + str(yd))
        print("u: " + str(u))
        print("w: " + str(w))
        print("ud: " + str(ud))
        print("wd: " + str(wd))
        print(currentPos)
        print(eMat)
        print iteration
        #colorVal = uint8()
        colorVal = 255-int(255*(math.sqrt(eMat[0,0]**2 + eMat[1,0]**2)/10))
        print colorVal
        setpen(255,colorVal,colorVal,5,0)
        controlMsg.linear.x=u #something
        controlMsg.linear.y=0
        controlMsg.linear.z=0
        controlMsg.angular.x=0
        controlMsg.angular.y=0
        controlMsg.angular.z=w #something
        pub.publish(controlMsg)
        iteration += 1
        xdold = xd
        ydold = yd
        t += dt
        tout.append(t)
        xout.append(currentPos.x)
        yout.append(currentPos.y)
        thetaout.append(currentPos.theta)
        if loop/4 > 9:
            plt.plot(tout, xout,'-', tout, yout, '-', tout, thetaout, '-')
            plt.show()
            return

        rate.sleep()

if __name__ == '__main__':
    listener()