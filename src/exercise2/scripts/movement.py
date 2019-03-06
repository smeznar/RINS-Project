#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import random

def rectangle_movement(step):

  twist = Twist()
  twist.linear.x = 0.1
  step = step % 20

  if step % 5 == 0:
    twist.linear.x = 0
    twist.angular.z = 1.57 #(90 / 360) * 2 * 3.14

  return twist


def circular_movement():
	twist = Twist()
	twist.linear.x = 1
	twist.angular.z = 3.14/2
	return twist


def triangular_movement(step):

  twist = Twist()
  twist.linear.x = 0.5
  step = step % 20

  if step % 5 == 0:
    twist.linear.x = 0
    twist.angular.z = 2.094 #(90 / 360) * 2 * 3.14

  return twist


def random_movement():
	twist = Twist()
	twist.linear.x = 1
	twist.angular.z = 2*random.random()*3.14 - 3.14
	return twist


def movement():

  pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1000)
  # For the turtle simulation map the topic to /turtle1/cmd_vel
  # For the turtlebot simulation and Turtlebot map the topic to /cmd_vel_mux/input/navi
  rospy.init_node('movement')

  r = rospy.Rate(1)

  step = 0.0

  while not rospy.is_shutdown():
    twist = random_movement()
    pub.publish(twist)
    step = step + 1.0
    r.sleep()

if __name__ == '__main__':
    movement()
