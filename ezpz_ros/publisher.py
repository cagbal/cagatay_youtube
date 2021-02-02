#!/usr/bin/env python

import rospy 

from std_msgs.msg import Int64


class MyNode(object):
    def __init__(self, node_name, topic_name):
        rospy.init_node(
            node_name,
            anonymous=True
        )
        
        self._publisher = rospy.Publisher(
            topic_name,
            Int64,
            queue_size=1
        )
        
    def publish(self, message):
        self._publisher.publish(message)
        
node = MyNode("my_node", "topic")
counter = 0

while counter < 10:
    node.publish(counter)
    counter += 1
    rospy.sleep(1)
