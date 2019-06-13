#!/usr/bin/env python

import rospy
import actionlib
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

goal_state = GoalStatus.LOST
goal_points = [(0.7,-0.28,0),(1.25,-1.47,1),(0,-3,1),(-0.8,-1.6,2),(1.9,-3.2,1)]

rospy.init_node('map_navigation', anonymous=False)

ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

while(not ac.wait_for_server(rospy.Duration.from_sec(2.0))):
              rospy.loginfo("Waiting for the move_base action server to come up")

for point in goal_points:
    goal_state = GoalStatus.LOST
    goal = MoveBaseGoal()

#Sending a goal to the to a certain position in the map
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = point[0]
    goal.target_pose.pose.position.y = point[1]
    goal.target_pose.pose.orientation.w = point[2]

    rospy.loginfo("Sending goal")
    ac.send_goal(goal)

    while (not goal_state == GoalStatus.SUCCEEDED):

        ac.wait_for_result(rospy.Duration(2))
        goal_state = ac.get_state()
        #Possible States Are: PENDING, ACTIVE, RECALLED, REJECTED, PREEMPTED, ABORTED, SUCCEEDED, LOST.

        if goal_state == GoalStatus.SUCCEEDED:
            rospy.loginfo("The goal was reached!")
        elif goal_state == GoalStatus.REJECTED or goal_state == GoalStatus.ABORTED or goal_state == GoalStatus.LOST:
            rospy.loginfo("Goal could not be reached!")
            break
        else:
            rospy.loginfo("Searching for the goal!")


GoalStatus.SUCCEEDED
