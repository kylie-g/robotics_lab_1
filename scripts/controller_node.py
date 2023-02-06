#!/usr/bin/env python3

import rospy
#subscribes to correct topic and recieves position information from the turtle_node
from turtlesim.msg import Pose 

from robotics_lab1.msg import Turtlecontrol

tc_msg = Turtlecontrol()

# recieves position information from the turtle_node
def pose_callback(data):
	tc_msg.kp = data.kp
	tc_msg.xd = data.xd
	rospy.loginfo("kp is %0.2f cm, xd is %0.2f cm", tc_msg.kp, tc_msg.xd)
	
if __name__ == '__main__':
	#creates a new topic and subscribes named /turtle1/control_params
	rospy.init_node('controller_node', anonymous = True)
	rospy.Subscriber('/turtle1/control_params', Turtlecontrol, pose_callback)

	#proportional control:
	pos_pub = rospy.Publisher('/turtle1/control_params', Turtlecontrol, queue_size = 10)
	loop_rate = rospy.Rate(10)
	#set up a loop that runs at thee 10Hz frequency
	while not rospy.is_shutdown():
		pos_pub.publish(tc_msg)
		loop_rate.sleep()
