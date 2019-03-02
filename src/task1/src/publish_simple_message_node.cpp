//Publishing randomly generated velocity messages for turtle-simulator

#include <ros/ros.h> // As previously said the standard ROS library
#include "task1/Test.h"

#include <sstream>

int main(int argc, char *argv[])
{
	ros::init(argc,argv,"simple_publisher"); //Initialize the ROS system, give the node the name "publish_velocity"
	ros::NodeHandle nh;	//Register the node with the ROS system

	//create a publisher object.
	ros::Publisher pub = nh.advertise<task1::Test>("sm_secret/simple_chat", 1000);	//the message tyoe is inside the angled brackets
																						//topic name is the first argument
																						//queue size is the second argument
	//Loop at 1Hz until the node is shutdown.
	ros::Rate rate(1);

	int seq = 0;
	while(ros::ok()){
		//Create the message.
		task1::Test msg;

		std::stringstream ss;

		ss << "secret message jnnsigsrpimrjnjna;efskopgsrops";
		msg.content=ss.str();
		msg.number=seq;
		seq += 1;

		//Publish the message
		pub.publish(msg);

		//Send a message to rosout
		ROS_INFO("%s with num %d", msg.content.c_str(), msg.number);

		//Wait untilit's time for another iteration.
		rate.sleep();
	}

	return 0;
}
