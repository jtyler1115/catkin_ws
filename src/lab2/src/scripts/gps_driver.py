#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import serial
import utm
from math import sin, pi
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from lab2.msg import Gps_data

def latlon_to_utm(latlon):
    print("here")
    '''
    Given pressure (in m fresh) and latitude (in radians) returns ocean
    depth (in m.).  Uses the formula discovered and presented by Leroy and
    Parthiot in: Claude C. Leroy and Francois Parthiot, 'Depth-pressure
    relationships in the oceans and seas', J. Acoustic Society of America,
    March 1998, p1346-.
    '''
    utmVal=utm.from_latlon(latlon[0],latlon[1])
    print(utmVal)
    print("/n")
    print(latlon)
    return utmVal


def parseInput(line):
    '''
    Takes $GPGGA string and converts it to a +/- based
    latitude and longitude
    '''
    dataList=line.split(",")
    latdeg=float(dataList[2][0:2])
    latmin=float(dataList[2][2:])
    lat = latdeg+(latmin/60)

    londeg=float(dataList[4][0:3])
    lonmin=float(dataList[4][3:])
    lon = londeg+(lonmin/60)
    if dataList[3]=="S":
        lat = -lat
    if dataList[5]=="W":
        lon = -lon
    alt = float(dataList[9])
    latlon = [lat, lon, alt]
    return latlon


if __name__ == '__main__':
    SENSOR_NAME = "gps"
    rospy.init_node('gps_driver')
    serial_port = rospy.get_param('~port','/dev/ttyUSB0')
    serial_baud = rospy.get_param('~baudrate',4800)
    sampling_rate = rospy.get_param('~sampling_rate',5.0)
  
    port = serial.Serial(serial_port, serial_baud, timeout=3.)
    rospy.logdebug("Using gps sensor on port "+serial_port+" at "+str(serial_baud))
   
    rospy.sleep(0.2)        
    
    gps_pub = rospy.Publisher(SENSOR_NAME, Gps_data, queue_size=5)
    
    rospy.logdebug("Initialization complete")
    
    rospy.loginfo("Publishing pressure and depth.")
    
    odom_msg = Odometry()
    odom_msg.header.frame_id = "odom"
    odom_msg.child_frame_id = SENSOR_NAME
    odom_msg.header.seq=0
    
    sleep_time = 1/sampling_rate - 0.025
    
    try:
        while not rospy.is_shutdown():
            line = port.readline()
            #dataList = line.split(",")
            if line == '':
                rospy.logwarn("GPS: No data")
            else:
                if line.startswith('$GPGGA'):
                    data_msg=Gps_data()
                    data_msg.header.stamp=rospy.Time.now() 
                    latlon = parseInput(line)
                    utmval = latlon_to_utm(latlon)
                    data_msg.latitude = latlon[0]
                    data_msg.longitude = latlon[1]
                    data_msg.altitude = latlon[2]
                    data_msg.utm_easting = utmval[0]
                    data_msg.utm_northing = utmval[1]
                    data_msg.zone = utmval[2]
                    data_msg.letter = utmval[3]
                    #print (latlon)               
                    gps_pub.publish(data_msg)
            rospy.sleep(sleep_time)
            
    except rospy.ROSInterruptException:
        port.close()
    
    except serial.serialutil.SerialException:
        rospy.loginfo("Shutting down gps_driver node...")

