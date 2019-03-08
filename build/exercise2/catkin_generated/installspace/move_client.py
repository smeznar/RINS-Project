#!/usr/bin/env python
# -*- Mode: Python; indent-tabs-mode: nil; c-basic-offset: 2; tab-width: 2 -*- *

import sys
import rospy
import random
from exercise2.srv import *

def moveT(shape, time):
  rospy.wait_for_service('move_service')
  try:
    move_serv = rospy.ServiceProxy('move_service', move)
    resp1 = move_serv(shape, time)
    return resp1.lastShape
  except rospy.ServiceException, e:
    print "Service call failed: %s"%e


if __name__ == "__main__":
	rospy.init_node('client_node')
	shapes = ["rectangle","triangle","circle","random"]

	r = rospy.Rate(0.06)
	while not rospy.is_shutdown():
		shape = shapes[random.randint(4)]
		time = random.randint(30)
		print "sending %s and %d"%(s ,t)
		print "result: %s"%(moveT(s, t))
		r.sleep()

	#if len(sys.argv) == 3:
	#	s = sys.argv[1]
	#	t = int(sys.argv[2])
	#else:
	#	print "not enough arguments"
	#	sys.exit(1)
	
  #s = "circle"
  #t = 10
	
	#s = rospy.get_param("move_type")
	#t = rospy.get_param("move_time")
	#print "sending %s and %d"%(s ,t)
	#print "result: %s"%(moveT(s, t))
  
  
