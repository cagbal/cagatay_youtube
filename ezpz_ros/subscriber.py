#!/usr/bin/env python

import rospy
from std_msgs.msg import Int64 

class Subscriber(object):
    def __init__(self, node_name, topic_name):
        rospy.init_node(
            node_name,
            anonymous=True
        )
        
        rospy.Subscriber(
            topic_name,
            Int64,
            self.callback
        )
        
    def callback(self, msg):
        print("Data: {}".format(msg.data))
        
    def run(self):
        rospy.spin()
        
node = Subscriber("my_sub", "my_topic")

node.run()
