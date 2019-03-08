#!/usr/bin/env python
# -*- Mode: Python; indent-tabs-mode: nil; c-basic-offset: 2; tab-width: 2 -*- *

from exercise2.srv import *
import rospy

def moveTurtle(req):
  previous_move = rospy.get_param("move_type")
	rospy.set_param("move_type", req.shape)
  rospy.set_param("move_time", req.time)
	print "move in shape: %s for %d seconds"%(req.shape, req.time)
	print "Returning %s"%(previous_move)
	return previous_move

def move_service():
  rospy.init_node('service_node')
  s = rospy.Service('move_service', move, moveTurtle)
  print "Ready to move."
  rospy.spin()

if __name__ == "__main__":
	move_service()
