#!/usr/bin/env python
import rospy 
import cv2

class AndroidCamera(object):
    def __init__(self, node_name, address):
        self._phone_address = address
        rospy.init_node(node_name, anonymous = False)
        self._device = cv2.VideoCapture(
            self._phone_address)   
        self._device.set(cv2.CAP_PROP_BUFFERSIZE, 0) 
        self._device.set(cv2.CAP_PROP_FRAME_WIDTH, 400) 
        self._device.set(cv2.CAP_PROP_FRAME_HEIGHT, 400) 
        rospy.sleep(1)

    def __del__(self):
        self._device.release()
    
    def get_frame(self):
        _, frame = self._device.read()
        
        return frame
                
    def run(self):
        while not rospy.is_shutdown():
            
            img = self.get_frame()
            
            cv2.imshow('frame',img)
            
            cv2.waitKey(10)
           
node = AndroidCamera(
    "camera_node", 
    "http://192.168.178.26:8080/video")
node.run()
