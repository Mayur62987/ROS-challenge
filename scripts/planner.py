#!/usr/bin/env python

import rospy
#########################################################################################define imports (sensors, clock, twist, range,vector3 and clock)
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
from std_msgs.msg import Bool
pub1 = None
global instruction
instruction = Twist()
global Acheck


def plan_clbck(msg):
	global instruction
	instruction = msg.data

def clbk_Avoidcheck(msg):
	global Acheck
	Acheck = msg.data

def decide():
	global instruction
	global Acheck
	msg1 = Twist() 
	linear_x = 0
	angular_z = 0

	#elif instruction == 20:
		#linear_x = 0.6
		#angular_z = 0.0
	if instruction == 70:
		linear_x = -0.3
		angular_z = 0.0	
	elif instruction == 13:
		linear_x = -0.3
		angular_z = 0.3
	elif instruction == 14:
		linear_x = -0.3
		angular_z = -0.3
	elif instruction == 10:
		linear_x = 0.4
		angular_z = 0.0
	elif instruction == 31:
		linear_x = 0
		angular_z = 0.3
	elif instruction == 32:
		linear_x = 0
		angular_z = -0.3
	elif instruction < 10:
		if (instruction % 2 == 0):
			linear_x = 0
			angular_z = -0.3
		else:
			linear_x = 0
			angular_z = 0.3

	msg1.linear.x = linear_x
	msg1.angular.z = angular_z
	#print (instruction)
	return msg1

def main():
	global yawcurrentintial 
	yawcurrentintial = False
	global pub1
	global pub2
	global robotstart
	#global yaw_current
	global yaw_intital 
	global state_
	global timestr
	robotstart = False
	rospy.init_node('motor_control')		 
	pub1 = rospy.Publisher('cmd_vel',Twist, queue_size = 1)
	sub_avoid = rospy.Subscriber('Avoidcheck',Bool, clbk_Avoidcheck)
	sub_plan = rospy.Subscriber('planner',Int32, plan_clbck)
	rate = rospy.Rate(50)
	

	while not rospy.is_shutdown():
		msg = Twist()
		msg = decide()
		pub1.publish(msg)
		rate.sleep()


if __name__ == '__main__':
	main() 
