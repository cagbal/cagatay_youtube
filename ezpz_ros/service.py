#!/usr/bin/env python

import rospy 

from std_srvs.srv import Trigger, TriggerResponse

import random 

RANDOM_GREETINGS = ["hi", "hello", "sup?", "yo!", "how's it going?"]

class GreetingsService(object):
    def __init__(self, node_name):
        rospy.init_node(
            node_name,
            anonymous=False
        )
        
        self._service = rospy.Service(node_name, Trigger, self.callback)
        
    def callback(self, request):
        response =  TriggerResponse()
        response.success = True
        response.message = random.choice(RANDOM_GREETINGS)
        
        return response 
    
    def run(self):
        rospy.spin()
        
service = GreetingsService("my_service")
service.run()
        
        