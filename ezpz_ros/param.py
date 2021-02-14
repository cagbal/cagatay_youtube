#!/usr/bin/env python

import rospy 

class ParameterParser(object):
    def __init__(self, node_name, param_name_list):
        self._parameter_names = param_name_list
        
        rospy.init_node(node_name, anonymous = False)
        
    def get_parameters(self):
        
        params = []
        
        for name in self._parameter_names:
            
            params.append(
                rospy.get_param(name, "no param :(")
            )
            
        return params
            
    def run(self):
        while not rospy.is_shutdown():
            print("********************")
            print(self.get_parameters())
            rospy.sleep(1)
        
        
node = ParameterParser("param_node", ["name", "age"])

node.run()