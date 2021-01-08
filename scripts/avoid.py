#!/usr/bin/env python

import rospy

from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Range
from std_msgs.msg import Int32
from std_msgs.msg import Bool
#from geometry_msgs.msg import Twist

pub1 = None
pub2 = None
global regions
global Avoidance
global check 
global revchek
global avoidtime
avoidtime = rospy.Time(0)
Avoidance = False
regions = {
 	'front1': 0, 
	'frontL': 0,
	'backL': 0,
 	'back1': 0,
	'back2': 0,
	'backR': 0,
	'frontR': 0,
	'front2' :0,
	}

fl = 0
fr = 0
rr = 0
rl = 0

def clbk_laser(msg):
	global regions
	regions = {
 	'front1': min(min(msg.ranges [0:90]), 12), 
	'frontL': min(min(msg.ranges[91:180]), 12),
	'backL': min(min(msg.ranges[181:270]), 12),
 	'back1': min(min(msg.ranges[271:360]), 12),
	'back2':  min(min(msg.ranges[361:450]), 12),
	'backR': min(min(msg.ranges[451:540]), 12),
	'frontR': min(min(msg.ranges[541:630]), 12),
	'front2' : min(min(msg.ranges[631:719]), 12),
	}

def clbk_fl(msg):
	global fl
	fl = msg.range

def clbk_fr(msg):
	global fr
	fr = msg.range

def clbk_rr (msg):
	global rr
	rr = msg.range

def clbk_rl (msg):
	global rl	
	rl = msg.range


def avoid():#regions, fl, fr, rl, rr):
	global fl      
	global fr 
	global rr
	global rl
	global regions
	global pub1
	global check 	
	check = 0
	global Avoidance
	Adur = rospy.Duration(10)
#	if regions['front1'] < 0.4 or regions['front2'] < 0.4 or fl < 0.32 or fr < 0.32 : #avoid m
#		if (regions['front1'] < 0.4 or regions['front2'] < 0.4) and (regions['frontL'] > 0.4 or regions['frontR'] > 0.4) and (regions['front1'] >= regions['front2']):
#				check = 1
#		elif (regions['front1'] < 0.4 or regions['front2'] < 0.4) and (regions['frontL'] > 0.4 or regions['frontR'] > 0.4) and (regions['front1'] < regions['front2']):
#				check = 2
#		elif (fl < 0.32 or fr < 0.32) and fl >= fr:
#			if ['front1'] >= regions['front2']:
#				check = 3
#			if ['front1'] < regions['front2']:	 
#				check = 4
#		elif (fl < 0.32 or fr < 0.32) and fl < fr:
#			if ['front1'] >= regions['front2']:
#				check = 5
#			if ['front1'] < regions['front2']:	
#				check = 6

	if regions['front1'] < 0.4 or regions['front2'] < 0.4 or fl < 0.32 or fr < 0.32 : #avoid m
		
		if Avoidance == True:
			avoidtime = rospy.Time.now()
	
			if (regions['front1'] < 0.4 or regions['front2'] < 0.4) and (regions['frontL'] > 0.4 or regions['frontR'] > 0.4) and (regions['front1'] >= regions['front2']):
				check = 1
			elif (regions['front1'] < 0.4 or regions['front2'] < 0.4) and (regions['frontL'] > 0.4 or regions['frontR'] > 0.4) and (regions['front1'] < regions['front2']):
				check = 2
			elif (fl < 0.32 or fr < 0.32) and fl >= fr:
				if ['front1'] >= regions['front2']:
					check = 3
				if ['front1'] < regions['front2']:	 
					check = 4
			elif (fl < 0.32 or fr < 0.32) and fl < fr:
				if ['front1'] >= regions['front2']:
					check = 5
				if ['front1'] < regions['front2']:	
					check = 6

			elif avoidtime < (rospy.Time.now() - tdur):
				Reversecheck()
	else:	
		Avoidance = False		
	return check

def Reversecheck():#regions, fl, fr, rl, rr):
	global fl      
	global fr 
	global rr
	global rl
	global regions
	global revcheck 
	
	if (rl >= 0.32 and rr >= 0.32) or (regions['back1'] >= 0.4 and regions['back1'] >= 0.4):
		if (regions['back1'] >= regions['back2']) and regions['backL'] <= 0.4:
			revcheck = 13
		elif (regions['back1'] < regions['back2']) and regions['backR'] <= 0.4:
			revcheck = 14
		else:
			revchek = 70

	return revcheck
		
def main():
	global pub1
	global regions
	global fl      
	global fr 
	global rr
	global rl
	global regions
	global check
	global avoidtime
	rospy.init_node('Avoid')
	sub_scan = rospy.Subscriber('scan',LaserScan, clbk_laser)		 
    	sub_f1 = rospy.Subscriber('range/fl',Range, clbk_fl)
   	sub_f2 = rospy.Subscriber('range/fr',Range, clbk_fr)
    	sub_r1 = rospy.Subscriber('range/rl',Range, clbk_rl)
    	sub_r2 = rospy.Subscriber('range/rr',Range, clbk_rr)
	pub1 = rospy.Publisher('planner',Int32, queue_size = 1)
	#pub1 = rospy.Publisher('cmd_vel',Twist, queue_size = 1)
	pub2 = rospy.Publisher('Avoidcheck',Bool,queue_size = 1)
	rate = rospy.Rate(50)
	

	while not rospy.is_shutdown(): 
		if regions['front1'] < 0.4 or regions['front2'] < 0.4 or fl < 0.32 or fr < 0.32:
			pub2.publish(True) ########true avoiding 
			msg =avoid()
			pub1.publish(msg)
		else:
			pub2.publish(False)
		#msg =avoid()
		#pub1.publish(msg)
		print(regions['front1'],regions['front2'],fl,fr,regions['frontL'],regions['frontR'],check)
		rate.sleep()

			
			
if __name__ == '__main__':
	main() 



