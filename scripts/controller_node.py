#!/usr/bin/env python3

import rospy

#imports:
from turtlesim.msg import Pose 

from geometry_msgs.msg import Twist

from robotics_lab1.msg import Turtlecontrol

#tc_msg to get xd (desired position) and kp (control gain)
tc_msg = Turtlecontrol()

#xt holds the positional information from the simulator
xt = float()


def control_param_callback(data):
	global tc_msg
	#get the control gain
	tc_msg.kp = data.kp
	#get the desired position
	tc_msg.xd = data.xd
	#rospy.loginfo("kp is %0.2f cm, xd is %0.2f cm", tc_msg.kp, tc_msg.xd)
	

# recieves position information from the turtle_node
def pose_callback(data):
	global xt
	#get the x data (positional info)
	xt = data.x
	
	
if __name__ == '__main__':
	#initialize the node
	rospy.init_node('controller_node', anonymous = True)
	
	#creates a new topic and subscribes named /turtle1/control_params - gets the desired position and control gain
	rospy.Subscriber('/turtle1/control_params', Turtlecontrol, control_param_callback)
	
	
	# add another subscriber for reading position info from the simulator
	# this subscribes to the correct topic (Pose) and recieves positional information from turtlesim_node
	rospy.Subscriber('/turtle1/pose', Pose, pose_callback)

	
	# update the publisher to send cmd_vel commands (topic, message)
	#publishes to velocity command topic
	pos_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
	
	# declare a variable of type Twist for sending control commands
	vel_cmd = Twist()
	
	#set up a loop that runs at thee 10Hz frequency
	loop_rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		# calculate the linear velocity (control equation) and put it into the linear x position
		vel_cmd.linear.x = (tc_msg.kp)*(tc_msg.xd-xt)
		# publish it
		pos_pub.publish(vel_cmd) # needs to be updated
		loop_rate.sleep()
