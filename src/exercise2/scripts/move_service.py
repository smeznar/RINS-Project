#!/usr/bin/env python

from exercise2.srv import *
import rospy

def moveTurtle(req):
	#s = sum(req.numbers)
	print "move in shape: %s for %d seconds"%(req.shape, req.time)
	#print "Returning %s"%(s)
	return req.shape

def move_service():
  rospy.init_node('service_node')
  s = rospy.Service('move_service', move, moveTurtle)
  print "Ready to move."
  rospy.spin()

if __name__ == "__main__":
	move_service()
