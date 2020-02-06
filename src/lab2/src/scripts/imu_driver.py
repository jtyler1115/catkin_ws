#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import serial
import re
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import Imu
from tf.transformations import quaternion_from_euler

def mag_to_quat(imu_raw):
    msg_out = Imu()
    msg_out.header.stamp=rospy.Time.now()
    
    yaw = float(imu_raw[1])
    pitch = float(imu_raw[2])
    roll = float(imu_raw[3])
    
    accx = float(imu_raw[7])
    accy = float(imu_raw[8])
    accz = float(imu_raw[9])
    
    gyrox = float(imu_raw[10])
    gyroy = float(imu_raw[11])
    gyroz = float(imu_raw[12])
    
    orientation = Quaternion()
    quat = quaternion_from_euler(roll,pitch,yaw)
    orientation.x = quat[0]
    orientation.y = quat[1]
    orientation.z = quat[2]
    orientation.w = quat[3]
    
    angular_velocity = Vector3()  
    angular_velocity.x = gyrox
    angular_velocity.y = gyroy
    angular_velocity.z = gyroz

    linear_acceleration = Vector3()
    linear_acceleration.x = accx
    linear_acceleration.y = accy
    linear_acceleration.z = accz

    msg_out.orientation = orientation
    msg_out.angular_velocity = angular_velocity
    msg_out.linear_acceleration = linear_acceleration

    return msg_out

def parseInput(line):
    '''
    Takes $vnymr string and converts it to a +/- based
    latitude and longitude
    '''
    print line
    cleanLine = line.replace('\x00','')
    #cleanLine2 = line.replace'\n','')
    dataList = re.split('[, \*]',cleanLine)
    print(dataList)
    return dataList


if __name__ == '__main__':
    SENSOR_NAME = "imu"
    rospy.init_node('imu_driver')
    serial_port = rospy.get_param('~port','/dev/ttyUSB0') ###### MIGHT HAVE TO CHANGE THIS
    serial_baud = rospy.get_param('~baudrate',115200)
    sampling_rate = rospy.get_param('~sampling_rate',5.0)
  
    port = serial.Serial(serial_port, serial_baud, timeout=3.)
    rospy.logdebug("Using gps sensor on port "+serial_port+" at "+str(serial_baud))
   
    rospy.sleep(0.2)        
    
    imu_pub = rospy.Publisher(SENSOR_NAME, Imu, queue_size=5)
    
    rospy.logdebug("Initialization complete")
    
    rospy.loginfo("Publishing IMU Data.")
    
    
    sleep_time = 1/sampling_rate - 0.025
    
    try:
        while not rospy.is_shutdown():
            line = port.readline()
            print("test")
            if line == '':
                rospy.logwarn("GPS: No data")
            else:
                if line.startswith('$VNYMR'): 
                    imu_raw = parseInput(line)
                    if len(imu_raw) == 14:
                        data_msg = mag_to_quat(imu_raw)           
                        imu_pub.publish(data_msg)
                    else:
                        rospy.logwarn("Bad Data: Reading next line")
            rospy.sleep(sleep_time)
            
    except rospy.ROSInterruptException:
        port.close()
    
    except serial.serialutil.SerialException:
        rospy.loginfo("Shutting down gps_driver node...")

