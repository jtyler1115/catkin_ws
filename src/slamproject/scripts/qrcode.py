#!/usr/bin/env python

from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import rospy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String
from std_msgs.msg import Bool
from cv_bridge import CvBridge, CvBridgeError
import time

pub = rospy.Publisher('scanner/barcode',String, queue_size=10)
output=String()
output="empty"
runstate=Bool()
runstate.data='false'
def decode(im) : 
    
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
 
# Print results
    decoded="empty"
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')
     
    return decodedObjects
 
 
# Display barcode and QR code location  
def display(im, decodedObjects):
 
#Loop over all decoded objects
    for decodedObject in decodedObjects: 
        points = decodedObject.polygon
 
        # If the points do not form a quad, find convex hull
        if len(points) > 4 : 
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else :
            hull = points;
     
        # Number of points in the convex hull
        n = len(hull)

        # Draw the convext hull
        for j in range(0,n):
            cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)
 
    # Display results 
    cv2.imshow("Results", im);
    cv2.waitKey(1);

def callback(data):
    global output
    start=time.time()
    image = CvBridge().compressed_imgmsg_to_cv2(data)
    #decode(image)
    #print(time.time()-start)
    cv2.imshow("th",image)
    cv2.waitKey(1)
    output = decode(image)
    #print(output)
    #display(image, decodedObjects)
def runstateCb(data):
    global runstate
    runstate=data.data

def listener():
    #global output
    #global runstate
    rospy.init_node("qrscanner",anonymous=True)
    rospy.Subscriber("camera/rgb/image_raw/compressed", CompressedImage, callback, queue_size=1)
    #rospy.Subscriber("scanner/runstate", Bool, runstateCb, queue_size=1)
    while not rospy.is_shutdown():
        pub.publish(output)
        rospy.sleep(.05)
   
# Main 
if __name__ == '__main__':
    listener()