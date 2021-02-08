#!/usr/bin/env python

import rospy 

from std_srvs.srv import Trigger

class FriendlyClient(object):
    def __init__(self, node_name, service_name):
        rospy.init_node(node_name)
        
        rospy.wait_for_service(service_name)
        
        self._service_run = rospy.ServiceProxy(
            service_name,
            Trigger)
           
    def call_service(self):
        result = self._service_run()
        print("Result: ", result)

node = FriendlyClient("my_client", "my_service")

for i in range(10):
    node.call_service()