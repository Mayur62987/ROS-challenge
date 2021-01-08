#include <ros/ros.h>     
#include <rosgraph_msgs/Clock.h>
#include <nav_msgs/Odometry.h>
#include <math.h>
//#include <geometry_msgs/Vector3.h>
#include <sensor_msgs/JointState.h>
#include "std_msgs/Float32.h"
//#include "std_msgs/Float64MultiArray.h"


ros::Time simTime;
double realTime;
double actTime;
double temptime;

geometry_msgs::Point prevPos;
sensor_msgs::JointState prevstate;
//geometry_msgs::Vector3 heading
double heading = 0.0;
bool robotstart = false;
bool Startime = false;
bool Robjst = false;
double totaldistance; 
double totalwd; 
double wheelR = 0.0425; //radius of wheel 

void myCallback(const rosgraph_msgs::Clock::ConstPtr &msg)
{
if (!Startime){
simTime = msg->clock;
temptime = simTime.toSec(); 
Startime = true;
realTime = simTime.toSec();
}

else {
simTime = msg->clock;
temptime = simTime.toSec();
actTime = temptime - realTime;

}


}

void rpy_callback(const geometry_msgs::Vector3::ConstPtr &rpy)
{
 heading = rpy->z;
}


void odomCallback(const nav_msgs::Odometry::ConstPtr &msg)
{
	if (!robotstart)
	{
		prevPos = msg->pose.pose.position;
		robotstart = true;
		//totaldistance = 0;

	} 


	else 
	{

		geometry_msgs::Point currPosition = msg->pose.pose.position;
		double distance = sqrt(pow(currPosition.x - prevPos.x ,2) + pow(currPosition.y - prevPos.y, 2));

		if (std::abs(distance) <= 0.0000001)
		{
			distance = 0.0;
		}


		totaldistance += std::abs(distance);

		prevPos = currPosition;

	}
}

void JointstateCallback(const sensor_msgs::JointState &msg)
{
	if (!Robjst)
	{       
		prevstate = msg;
		Robjst = true;
		std::cout << "hello: " << std::endl;
	} 

	else 
	{

		sensor_msgs::JointState currstate = msg;
		double fl = std::abs(currstate.position[0] - prevstate.position[0])*wheelR;
		double fr = std::abs(currstate.position[1] - prevstate.position[1])*wheelR;
		double rl = std::abs(currstate.position[2] - prevstate.position[2])*wheelR;
		double rr = std::abs(currstate.position[3] - prevstate.position[3])*wheelR;
		
	        double avedist = ((fl+fr+rl+rr)/4); 

		totalwd += std::abs(avedist);
		prevstate = currstate;
		
	}
}



int main(int argc, char **argv)
{
	ros::init(argc, argv, "monitor_node");
//ros::init(argc, argv, "displacement_node");
	ros::NodeHandle n("~");
	ros::Subscriber sub = n.subscribe("/clock", 10, myCallback);
	ros::Subscriber odomsub = n.subscribe("/odom", 10, odomCallback);
	ros::Subscriber headingsub = n.subscribe("/rpy", 10, rpy_callback);
	ros::Subscriber jointstatesub = n.subscribe("/joint_states", 10, JointstateCallback);
	ros::Rate loop_rate(100);
	int counter = 25;
	while (ros::ok())
	{      
		++counter;
		ros::spinOnce();
		loop_rate.sleep();
		if (counter > 50)
		{
			counter = 0;
			std::cout << "Simulation Time:   " << actTime << std::endl;
			std::cout << "Distance traveled: " << totaldistance << std::endl;
			std::cout << "heading: " << heading << std::endl;
			std::cout << "total wheel distance: " << totalwd << std::endl;
			std::cout << "~~~~~~~~~~~~~~~~~~~~~"<< std::endl;
			
		}
	}
}
