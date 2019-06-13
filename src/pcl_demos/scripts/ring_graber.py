#!/usr/bin/env python
import sys
import rospy
import numpy as np
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose
from pcl_demos.msg import RingPose
from nav_msgs.msg import OccupancyGrid
ring_start = []


class Ring_grabber:
    def __init__(self):
        self.poligon_map = list()
        rospy.init_node("ime",anonymous = True)
        rospy.Subscriber("grab_3d_ring", RingPose, self.grab_3d_ring_callback)
        rospy.Subscriber("map", OccupancyGrid, self.map_callback)


    def grab_3d_ring_callback(self, msg):
        print (msg.x, msg.y,msg.r)

    def map_callback(self, grid):
        size_x = grid.info.width
        size_y = grid.info.height
        if (size_x < 3) or (size_y < 3):
            print("Map size is only x: %d,  y: %d . Not running map to image conversion", size_x, size_y)
            return

        self.map_resolution = grid.info.resolution
        self.originX = grid.info.origin.position.x
        self.originY = grid.info.origin.position.y
        map_array = grid.data

        size_y_rev = size_y - 1

        self.poligon_map = [[0 for _ in range(size_x)] for _ in range(size_y)]
        self.rings_map = [[0 for _ in range(size_x)] for _ in range(size_y)]
        # transformira mapo
        for y in reversed(range(size_y_rev)):
            idx_img_y = size_x * y
            for x in range(size_x):
                idx = idx_img_y + x
                # print(idx)
                if map_array[idx] == -1:
                    self.poligon_map[y][x] = 127
                elif map_array[idx] == 0:
                    self.poligon_map[y][x] = 255
                else:
                    self.poligon_map[y][x] = 0

if __name__ == '__main__':
    ring_Grabber = Ring_grabber()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("bla bla")
