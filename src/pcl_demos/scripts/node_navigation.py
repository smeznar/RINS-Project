#!/usr/bin/env python

import sys
import random
import rospy
import actionlib
import time
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from tf.transformations import quaternion_from_euler
from pcl_demos.msg import RingPose
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2, sqrt
import math

# (0.7,-0.28,1),
# goal_points = [(1.25, -1.47, 1),(1.25, -1.47, 0.5),(1.25, -1.47, 0), (0, -3, 1), (-0.8, -1.6, 2), (1.9, -3.2, 1)]

graph = None
# Lahko spremenimo direkt v tocke
areas = [[0.55, -0.35, 0, 0.5], [-0.74, -1.91, 0, 0.5], [0.54, -2.39, 0, 0.25],
         [1.15, -1.61, 0, 0.5], [1.68, -3.13, 0, 0.3], [0.08, -3.72, 0, 0.5]]

ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)
goal_state = GoalStatus.LOST

ring_points = []
last_circle = -1
circle_interrupt = False
last_pos = None

# Ring stuff
ring_detected = False
position = -1
ring_position = -1
twist_pub = None


class Area:
    def __init__(self, x, y, rot, weight):
        self.x = x
        self.y = y
        self.rot = rot
        self.weight = weight  # For selecting some more likely lower better
        self.visited = 0

    def get_area_point(self):
        # x_rand = random.random()
        # y_rand = random.random()
        # rotation_rand = random.random()
        # x = abs(self.x1 - self.x2) * x_rand + min(self.x1, self.x2)
        # y = abs(self.y1 - self.y2) * y_rand + min(self.y1, self.y2)
        # rotation = 6.28*rotation_rand
        return [self.x, self.y, self.rot]

    def times_visited(self):
        return self.visited * self.weight


class PathGraph:
    def __init__(self):
        global areas
        self.areas = self.generate_areas(areas)
        self.connections = {0: [1], 1: [0, 2], 2: [1, 3, 4, 5], 3: [2, 4], 4: [2, 3, 5], 5: [2, 4]}
        self.current_area = 2

    def generate_areas(self, ar):
        ars = list()
        for a in ar:
            ars.append(Area(a[0], a[1], a[2], a[3]))
        return ars

    def goal_reached(self):
        self.rotate()
        self.areas[self.current_area].visited += 1

    def select_next_point(self):
        cons = self.connections[self.current_area]
        score = 1000
        points = list()
        for i in cons:
            a = self.areas[i]
            if a.times_visited() < score:
                points = [i]
                score = a.times_visited()
            elif a.times_visited() == score:
                points.append(i)
        point = points[random.randint(0, len(points) - 1)]
        self.current_area = point
        return self.areas[point].get_area_point()

    def rotate(self):
        rot = 0
        twist = Twist()
        r = rospy.Rate(10)
        while rot < 6.28:
            twist.linear.x = 0.0
            twist.angular.z = 0.5
            twist_pub.publish(twist)
            rot += 0.05
            r.sleep()


def say_ring(sentence):
    sound_handle = SoundClient()
    rospy.sleep(1)

    voice = 'voice_kal_diphone'
    volume = 1.0

    sound_handle.say(sentence, voice, volume)
    rospy.sleep(1)


def go_trough_goals():
    global last_pos, circle_interrupt, ac, graph, goal_state, ring_detected
    if last_pos is None:
        last_pos = graph.select_next_point()
    while not ring_detected:
        point = last_pos
        goal_state = GoalStatus.LOST
        goal = MoveBaseGoal()

        # Sending a goal to the to a certain position in the map
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = point[0]
        goal.target_pose.pose.position.y = point[1]
        gt = quaternion_from_euler(0, 0, point[2])
        goal.target_pose.pose.orientation.x = gt[0]
        goal.target_pose.pose.orientation.y = gt[1]
        goal.target_pose.pose.orientation.z = gt[2]
        goal.target_pose.pose.orientation.w = gt[3]

        rospy.loginfo("Sending goal")
        ac.send_goal(goal)

        while not goal_state == GoalStatus.SUCCEEDED:

            ac.wait_for_result(rospy.Duration(2))
            goal_state = ac.get_state()
            # Possible States Are: PENDING, ACTIVE, RECALLED, REJECTED, PREEMPTED, ABORTED, SUCCEEDED, LOST.
            if ring_detected:
                rospy.loginfo("Ring detected!")
                break
            if circle_interrupt:
                rospy.loginfo("Found circle and interrupted the goal!")
                find_circle()
            if goal_state == GoalStatus.SUCCEEDED:
                # say_ring()
                time.sleep(5)
                rospy.loginfo("The goal was reached!")
            elif goal_state == GoalStatus.REJECTED or goal_state == GoalStatus.ABORTED or goal_state == GoalStatus.LOST:
                rospy.loginfo("Goal could not be reached!")
                break
            else:
                rospy.loginfo("Searching for the goal!")
        if not ring_detected:
            last_pos = graph.select_next_point()
        else:
            break
    position_for_ring()


def circle_callback(msg):
    global circle_interrupt, last_pos, goal_state, ring_points, ac
    position = msg.position
    goal = MoveBaseGoal()

    # Sending a goal to the to a certain position in the map
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = position.x
    goal.target_pose.pose.position.y = position.y
    # TODO: fix orientation
    goal.target_pose.pose.orientation.x = msg.orientation.x
    goal.target_pose.pose.orientation.y = msg.orientation.y
    goal.target_pose.pose.orientation.z = msg.orientation.z
    goal.target_pose.pose.orientation.w = msg.orientation.w
    ring_points.append(goal)
    circle_interrupt = True


def find_circle():
    global circle_interrupt, last_pos, goal_state, ring_points, ac, last_circle, ring_detected
    goal_state = GoalStatus.PENDING
    i = last_circle + 1
    while i < len(ring_points) and not ring_detected:
        last_circle = i
        ac.send_goal(ring_points[i])
        while not (goal_state == GoalStatus.SUCCEEDED):

            ac.wait_for_result(rospy.Duration(2))
            goal_state = ac.get_state()
            # Possible States Are: , ACTIVE, RECALLED, REJECTED, PREEMPTED, ABORTED, SUCCEEDED, LOST.
            if ring_detected:
                last_circle -= 1
                break
            if goal_state == GoalStatus.SUCCEEDED:
                rospy.loginfo("The ring was reached!")
                if last_circle == 2:
                    say_ring('i have found all circles')
                    sys.exit()
                else:
                    say_ring('i have found a circle')
                # say_ring('i have found a circle')
                break
            elif goal_state == GoalStatus.REJECTED or goal_state == GoalStatus.ABORTED or goal_state == GoalStatus.LOST:
                rospy.loginfo("ring could not be reached!")
                break
            else:
                rospy.loginfo("Searching for the goal(ring)!")
        if not ring_detected:
            goal_state = GoalStatus.PENDING
            i += 1
    if not ring_detected:
        circle_interrupt = False
        go_trough_goals()


def ring_interrupt(msg):
    global ring_detected, position, ring_position
    ring_detected = True
    position = [msg.x_pred, msg.y_pred, msg.ori_pred]
    ring_position = [msg.x_ring, msg.y_ring]


def position_for_ring():
    global position, ac, goal_state
    if position != -1:
        goal_state = GoalStatus.LOST
        goal = MoveBaseGoal()

        # Sending a goal to the to a certain position in the map
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = position[0]
        goal.target_pose.pose.position.y = position[1]
        gt = quaternion_from_euler(0, 0, position[2])
        goal.target_pose.pose.orientation.x = gt[0]
        goal.target_pose.pose.orientation.y = gt[1]
        goal.target_pose.pose.orientation.z = gt[2]
        goal.target_pose.pose.orientation.w = gt[3]

        rospy.loginfo("Sending Ring goal")
        ac.send_goal(goal)

        while not goal_state == GoalStatus.SUCCEEDED:

            ac.wait_for_result(rospy.Duration(2))
            goal_state = ac.get_state()
            # Possible States Are: PENDING, ACTIVE, RECALLED, REJECTED, PREEMPTED, ABORTED, SUCCEEDED, LOST.
            if goal_state == GoalStatus.SUCCEEDED:
                # say_ring()
                rospy.loginfo("Positioned to grab!")
                get_ring_rot()
                break
            elif goal_state == GoalStatus.REJECTED or goal_state == GoalStatus.ABORTED or goal_state == GoalStatus.LOST:
                rospy.loginfo("Better fix our goal :/ !")
                break
            else:
                rospy.loginfo("Searching for the goal!")
    else:
        go_trough_goals()
    go_trough_goals()


def get_ring():
    global ring_position, position, twist_pub, ring_detected
    goal_x = ring_position[0]
    goal_y = ring_position[1]
    rot = position[2]
    pos_x = position[0]
    pos_y = position[1]
    twist = Twist()
    angle_to_goal = atan2(goal_y - pos_y, goal_x - pos_x)
    if angle_to_goal < 0:
        angle_to_goal += 2 * 3.14
    distance = sqrt(pow((goal_x - pos_x), 2) + pow((goal_y - pos_y), 2)) + 0.4
    current_distance = 0
    r = rospy.Rate(25)
    print(angle_to_goal)
    for i in [-0.3,-0.25,-0.2,-0.15,-0.08, -0.02, 0.01, 0.04 ]:

        while abs(angle_to_goal + i - rot) %(2*3.14) > 0.01:
            #print("rotating",abs(angle_to_goal + i - rot)%(2*3.14))
            twist.linear.x = 0.0
            twist.angular.z = 0.2
            twist_pub.publish(twist)
            rot = rot + 0.008
            r.sleep()

        current_distance = 0
        while current_distance < distance:
            print("going forward")
            twist.linear.x = 0.5
            twist.angular.z = 0.0
            twist_pub.publish(twist)
            current_distance += 0.02
            r.sleep()

        current_distance = 0
        while current_distance < distance:
            print("going forward")
            twist.linear.x = -0.5
            twist.angular.z = 0.0
            twist_pub.publish(twist)
            current_distance += 0.02
            r.sleep()
        twist.angular.z = 0
        twist.angular.x = 0
    twist_pub.publish(twist)
    ring_detected = False
    go_trough_goals()

def get_ring_rot():
    global ring_position, position, twist_pub, ring_detected
    goal_x = ring_position[0]
    goal_y = ring_position[1]
    rot = position[2]
    pos_x = position[0]
    pos_y = position[1]
    twist = Twist()
    angle_to_goal = atan2(goal_y - pos_y, goal_x - pos_x)
    if angle_to_goal < 0:
        angle_to_goal += 2 * math.pi
    distance = sqrt(pow((goal_x - pos_x), 2) + pow((goal_y - pos_y), 2)) + 0.4
    current_distance = 0
    r = rospy.Rate(25)
    print(angle_to_goal)
    # obrne proti njemu
    while abs(angle_to_goal - rot) % (2 * math.pi) > 0.01:
        # print("rotating",abs(angle_to_goal + i - rot)%(2*3.14))
        twist.linear.x = 0.0
        twist.angular.z = 0.2
        twist_pub.publish(twist)
        rot = rot + 0.008
        r.sleep()

    for i in range(4):
        print (360)
        rot = 0
        while abs(2*math.pi+0.2 - rot) > 0.01:
            # print("rotating",abs(angle_to_goal + i - rot)%(2*3.14))
            twist.linear.x = 0.0
            twist.angular.z = 1
            twist_pub.publish(twist)
            rot = rot + 0.04
            r.sleep()
        for j in range(3):
            print("going forward")
            twist.linear.x = 0.5
            twist.angular.z = 0.0
            twist_pub.publish(twist)
            r.sleep()

    for j in range(4):
        print("going forward")
        twist.linear.x = -0.5
        twist.angular.z = 0.0
        twist_pub.publish(twist)
        r.sleep()
    twist.angular.z = 0
    twist.linear.x = 0

    twist_pub.publish(twist)
    ring_detected = False
    go_trough_goals()


if __name__ == '__main__':
    global goal_state, graph, ac
    rospy.init_node('map_navigation', anonymous=False)

    circle_detect = rospy.Subscriber("/ring_detection", Pose, circle_callback)
    ring_detect = rospy.Subscriber("/ring_located", RingPose, ring_interrupt)
    twist_pub = rospy.Publisher("/cmd_vel_mux/input/navi", Twist, queue_size=10)

    while not ac.wait_for_server(rospy.Duration.from_sec(2.0)):
        rospy.loginfo("Waiting for the move_base action server to come up")

    graph = PathGraph()
    go_trough_goals()
    goal_state = GoalStatus.SUCCEEDED
