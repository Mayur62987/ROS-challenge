#!/usr/bin/env python

import rospy

from geometry_msgs.msg import Vector3
from std_msgs.msg import Int32 
from std_msgs.msg import Bool 

global regions
global yaw_allowance
yaw_allowance = 4
global Acheck
global Bcheck
global Ccheck
global timestr
timestr = rospy.Time(0)
Acheck = False
#Bcheck = False
#Ccheck = False
global state_
global strtime
global isstr
strtime = True

state_ = 1

def change_state(state):
	global state_,state_dict
	if state is not state_:
		print 'rosbot - [%s] - %s' % (state, state_dict_[state])
		state_ = state


state_dict_= {
	0 : 'correct yaw',
	1 : 'go_str',
}


def clbk_yawcorrection(msg):
	global yaw_initial
	global yaw_current
	global robotstart  
	global yawcurrentintial
	

	if robotstart == False:
		yaw_initial = msg.z
		yaw_current = yaw_initial
		robotstart = True
		yawcurrentintial = True

	else:
		yaw_current = msg.z

def clbk_Avoidcheck(msg):
	global Acheck
	global Bcheck
	global Ccheck
	global timestr
	Acheck = msg.data
	

	
def yaw_correction(yaw_current):
	global Acheck
	global yaw_initial
	global robotstart 
	global pub
	global yaw_differencetemp
	global yaw_differenceact
	global pub1
	check = 0
	global temptwist
	global p	
	global isstr
	#global yaw_current
	#p = 0.02
	

	yaw_differencetemp = yaw_current - yaw_initial ###get detla yaw
	
	if yaw_differencetemp < 0:	
		yaw_differenceact = 360 - abs(yaw_differencetemp)
	else:
	   yaw_differenceact = yaw_differencetemp
	
	
	
	if (yaw_differenceact > yaw_allowance) and yaw_differenceact >= 180:
		#twist_msg.linear.x = 0.2
		#temptwist = (p*yaw_differenceact)
		#if temptwist <= 0.1:
			#twist_msg.angular.z = 0.2
		#if temptwist >= 0.6:
			#twist_msg.angular.z = 0.5
		#else:
			#twist_msg.angular.z = temptwist
		#twist_msg.angular.z = 0.4
		check = 31
		isstr = False

		
	elif (yaw_differenceact > yaw_allowance) and yaw_differenceact < 180:
		#twist_msg.linear.x = 0.2
		#temptwist = -(p*yaw_differenceact)
		#if temptwist >= -0.1:
			#twist_msg.angular.z = -0.2
		#if temptwist <= -0.6:
			#twist_msg.angular.z = -0.5
		#else:
			#twist_msg.angular.z = temptwist
		#twist_msg.angular.z = -0.4 
		check = 32
		isstr = False
	
	elif yaw_differenceact <= yaw_allowance:
		isstr = True
		
#	print yaw_differenceact
#	print Acheck	
	return check


def gostraight():
	global state_
	global Acheck
	check = 0
	global timestr
	global strtime
	global tdur
	global isstr
	global yaw_current
	tdur = rospy.Duration(1.5)
	##tspeed = rospy.Duration(4)
#	print(Acheck)
#	print(isstr)
#	print(strtime)
	
	if Acheck == False : #nothing left or right go straight
		
		check = 10
		
		if strtime == True:
			timestr = rospy.Time.now()
			strtime = False
			##change_state(1)
			print("timerstart")
			
		elif timestr < (rospy.Time.now() - tdur):	## timestr < rospy.Time.now() - tdur ##timestrnot defined
#			change_state(0)
			check = yaw_correction(yaw_current)
#			check = 10
			print("Timercheck")
			if isstr:
				strtime = True
			
		elif timestr > (rospy.Time.now() - tdur):
			print("breaK")
			check = yaw_correction(yaw_current)
			check = 10
			if isstr:
				strtime = True
	else:
#		check = yaw_correction(yaw_current)
#		if (isstr or Acheck) and strtime == False:
#						
		strtime = True
		print("timereset")
	
			 
				

		#elif timestr < (rospy.Time.now() - tspeed): # ramp straight speed when going straight for longer than 2 seconds
			#check = 20	

	return check	


def main():
	global yawcurrentintial 
	yawcurrentintial = False
	global Ccheck
	global pub1
	global pub2
	global robotstart
	global yaw_intital 
	global state_
	global timestr
	global yaw_differenceact
	global tur
	global isstr
	isstr = True
	robotstart = False
	rospy.init_node('Yaw_check')
	sub_yaw = rospy.Subscriber('/rpy',Vector3, clbk_yawcorrection)
	sub_avoid = rospy.Subscriber('Avoidcheck',Bool, clbk_Avoidcheck)
	pub1 = rospy.Publisher('planner',Int32, queue_size = 1)
	rate = rospy.Rate(20)
	

	while not rospy.is_shutdown():
		msg = gostraight()
		if Acheck == False:
			
#			if state_ == 0 and yawcurrentintial == True:
#				msg = yaw_correction(yaw_current)
#			elif state_ == 1:
#				msg = gostraight()
#			else: 	
#				print('Unknown state!!!!')
		#print("State is: %x" %state_)
		#print(msg)
			pub1.publish(msg)
		rate.sleep()
		
				 

if __name__ == '__main__':
	main() 

