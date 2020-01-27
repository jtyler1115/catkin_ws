#!/usr/bin/env python

import rospy
from std_msgs.msg import String
print("setup")
configs = rospy.get_param('color_list')
colorlist = configs['colors']

def talker():
    pub = rospy.Publisher("chatter", String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)
    print("test")
    idx = 0

    while not rospy.is_shutdown():
        color = colorlist[idx%4]
        hello_str = "Hello, color is " + color
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        idx += 1
        rate.sleep()

if __name__=='__main__':
    print("AHHH")
    try:
        talker()
    except rospy.ROSInitException:
        pass