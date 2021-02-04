#!/usr/bin/env python

import rospy 

class MyNode(object):
    def __init__(self, 
                 node_name, 
                 anonymous):
        rospy.init_node(
            node_name,
            anonymous=anonymous
        )
        
node_0 = MyNode("my_node", False) 

rospy.spin()

 
