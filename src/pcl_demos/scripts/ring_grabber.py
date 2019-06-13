#!/usr/bin/env python

import sys
import rospy
import numpy as np
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose
from pcl_demos.msg import RingPose
from nav_msgs.msg import OccupancyGrid

# from joblib import dump, load
ring_start = []

from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2, sqrt
import numpy as np
from sklearn.svm import NuSVC
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import PointStamped, Vector3, Pose
from std_msgs.msg import ColorRGBA
from sklearn.ensemble import RandomForestClassifier

# 0                             1                        2                      3
area = [[(236, 220), (245, 236)], [(234, 205), (244, 220)], [(246, 201), (256, 216)], [(250, 178), (260, 190)],
        # 4                     5                     6                          7
        [(245, 163), (257, 179)], [(260, 155), (270, 174)], [(262, 174), (270, 189)], [(272, 190), (278, 201)]]

# [(102,105,116),(103,101,117),(61,54,69),(62,59,76),(124,126,136),(100,98,113)]


class RingGrabber:
    def __init__(self):
        rospy.init_node("ime", anonymous=True)
        self.marker_array = MarkerArray()
        self.markers_num = 1
        self.accumulator = {}
        self.poligon_map = list()
        self.areaFound = [False, False, False, False, False, False, False, False]
        self.box_rviz = [(0.23, -1.26), (0.9, -3.396), (1.92, -2.17)]
        self.map_resolution = 1
        self.originX = 0
        self.originY = 0
        self.rings_map = list()
        rospy.Subscriber("grab_3d_ring", RingPose, self.grab_3d_ring_callback)
        rospy.Subscriber("map", OccupancyGrid, self.map_callback)
        self.ring_pub = rospy.Publisher("/ring_located", RingPose, queue_size=10)
        self.markers_pub = rospy.Publisher('ring_markers', MarkerArray, queue_size=1000)

    def grab_3d_ring_callback(self, msg):
        # msg.x v rviz -> x v matriki
        x = int((msg.x_ring - self.originX) / self.map_resolution)
        y = int((msg.y_ring - self.originY) / self.map_resolution)

        if (x, y) in self.accumulator:
            self.accumulator[(x, y)].append((msg.r, msg.g, msg.b))
            if len(self.accumulator[(x, y)]) > 2:
                r = sum([r for r, g, b in self.accumulator[(x, y)]]) / len(self.accumulator[(x, y)])
                g = sum([g for r, g, b in self.accumulator[(x, y)]]) / len(self.accumulator[(x, y)])
                b = sum([b for r, g, b in self.accumulator[(x, y)]]) / len(self.accumulator[(x, y)])
                r, g, b, color = self.find_color(r, g, b)
                if self.find_predefined_position(x, y, r, g, b):
                    ret = self.find_predef_rot(x, y)
                    if ret is None:
                        print("[Ring] Vrne none")
                        return
                    else:
                        x_ret, y_ret = ret
                    xrviz = x_ret
                    yrviz = y_ret
                    goals_msg = RingPose()
                    goals_msg.x_ring = msg.x_ring
                    goals_msg.y_ring = msg.y_ring
                    goals_msg.x_pred = xrviz
                    goals_msg.y_pred = yrviz
                    goals_msg.ori_pred = 0
                    goals_msg.r = r
                    goals_msg.g = g
                    goals_msg.b = b
                    goals_msg.color = color
                    print("[Ring] Publish point", xrviz, yrviz)
                    self.ring_pub.publish(goals_msg)

        else:
            self.accumulator[(x, y)] = list()
            self.accumulator[(x, y)].append((msg.r, msg.g, msg.b))

    def find_predefined_position(self, x_mat, y_mat, r, g, b):
        global area
        for i in range(len(area)):
            l = area[i]
            x1, y1 = l[0]
            x2, y2 = l[1]
            if x1 <= x_mat <= x2 and y1 <= y_mat <= y2:
                if not self.areaFound[i]:
                    xrviz = x_mat * self.map_resolution + self.originX
                    yrviz = y_mat * self.map_resolution + self.originY
                    print("barva ringa",r,g,b)
                    self.send_marker(xrviz, yrviz, r, g, b)
                    self.areaFound[i] = True
                return True
        return False

    def find_predef_rot(self, x_mat, y_mat):
        xrviz = x_mat * self.map_resolution + self.originX
        yrviz = y_mat * self.map_resolution + self.originY
        dist_list = [np.sqrt((x - xrviz) ** 2 + (y - yrviz) ** 2) for x, y in self.box_rviz]
        index = int(np.argmin(dist_list))
        x, y = self.box_rviz[index]
        dist = dist_list[index]
        dx = (xrviz - x) / dist
        dy = (yrviz - y) / dist
        k = 0.15
        x_new = xrviz + k * dx
        y_new = yrviz + k * dy
        return x_new, y_new  # rvizkoordinate

    def find_color(self, r_point, g_point, b_point):
        global red,green,blue,black
        barve_name = ["red", "green", "blue", "black"]
        maks = int(np.max([r_point, g_point, b_point]))
        mini = int(np.min([r_point, g_point, b_point]))
        print("razmerje:",maks*1.0/mini,mini*1.0/maks,"mini:",mini,"maks:",maks)
        if maks*1.0/(1+mini) < 4 and r_point+g_point+b_point < 400:
            return 255, 255, 255, 'black'
        index = int(np.argmax([r_point, g_point, b_point]))
        print("[Ring] Ring color is -> ", barve_name[index])
        barve = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
        return barve[index][0], barve[index][1], barve[index][2], barve_name[index]

    def send_marker(self, x, y, r, g, b):
        print("[Ring] Sending marker")
        point_s = PointStamped()
        point_s.point.x = x
        point_s.point.y = y
        point_s.point.z = 0
        point_s.header.stamp = rospy.Time(0)

        pose = Pose()
        pose.position.x = x
        pose.position.y = y
        pose.position.z = 0
        marker = Marker()
        marker.header.stamp = rospy.Time(0)
        marker.header.frame_id = "map"
        marker.pose = pose
        marker.type = Marker.CUBE
        marker.action = Marker.ADD
        marker.frame_locked = False
        marker.lifetime = rospy.Time(1000)
        marker.id = self.markers_num
        marker.scale = Vector3(0.2, 0.2, 0.2)
        marker.color = ColorRGBA((1.0*r) / 255, (1.0*g) / 255, (1.0*b) / 255, 1)
        self.marker_array.markers.append(marker)
        self.markers_num += 1
        self.markers_pub.publish(self.marker_array)

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


class DetectCylinder:
    def __init__(self):
        rospy.init_node("ime", anonymous=True)
        self.marker_array = MarkerArray()
        self.markers_num = 1
        self.accumulator = {}
        self.poligon_map = list()
        self.map_resolution = 1
        self.originX = 0
        self.originY = 0
        self.rings_map = list()
        self.area_cylinder = [(0.5, -2.6, -0.8, -5), (0.5, -2.6, 2.6, -4.2), (0.5, -2.6, 2.0, -0.7),
                              (0.5, -2.6, -1.9, -0.8), (1.6, 0.5, -0.1, -0.9)]
        rospy.Subscriber("grab_cylinder", RingPose, self.grab_cylinder)
        rospy.Subscriber("map", OccupancyGrid, self.map_callback)
        self.cylinder_pub = rospy.Publisher("/cylinder_located", RingPose, queue_size=10)
        self.markers_pub = rospy.Publisher('cylinder_markers', MarkerArray, queue_size=1000)

    def grab_cylinder(self, msg):
        # msg.x v rviz -> x v matriki
        x = int((msg.x_ring - self.originX) / self.map_resolution)
        y = int((msg.y_ring - self.originY) / self.map_resolution)

        if (x, y) in self.accumulator:
            if self.accumulator[(x, y)] == -1:
                print("[Cylinder] Ze zaznan cilinder")
                return
            self.accumulator[(x, y)].append((msg.r, msg.g, msg.b,msg.x_ring, msg.y_ring))
            okolica = list()
            s = 5
            for i in range(-s, s+1):
                for j in range(-s, s+1):
                    if (x+i, y+j) in self.accumulator:
                        if self.accumulator[(x+i, y+j)] == -1:
                            print("[Cylinder] Ze zaznan cilinder v tej blizini")
                            return
                        okolica = okolica+self.accumulator[(x+i, y+j)]
            if len(okolica) > 2:
                r = sum([r for r, g, b, tmp, tmp2 in okolica]) / len(okolica)
                g = sum([g for r, g, b, tmp, tmp2 in okolica]) / len(okolica)
                b = sum([b for r, g, b, tmp, tmp2 in okolica]) / len(okolica)
                # print("barva: ", r, g, b)
                r, g, b, color = self.find_color(r, g, b)
                print("[Cylinder] Cilinder je barve: ", color)
                x_avg = np.mean([tmp for r, g, b,tmp,tmp2 in okolica])
                y_avg = np.mean([tmp2 for r, g, b,tmp,tmp2 in okolica])
                ret = self.find_predef_rot(x_avg, y_avg)
                if ret is None:
                    print("[Cylinder] Ne najde rotacije")
                    return
                else:
                    x_ret, y_ret, ori = ret
                self.send_marker(x_ret, y_ret, r, g, b)
                goals_msg = RingPose()
                goals_msg.x_ring = msg.x_ring
                goals_msg.y_ring = msg.y_ring
                goals_msg.x_pred = x_ret
                goals_msg.y_pred = y_ret
                goals_msg.ori_pred = ori
                goals_msg.r = r
                goals_msg.g = g
                goals_msg.b = b
                goals_msg.color = color
                self.cylinder_pub.publish(goals_msg)
                s = 10
                for i in range(-s, s+1):
                    for j in range(-s, s+1):
                        self.accumulator[(x+i, y+j)] = -1
        else:
            self.accumulator[(x, y)] = list()
            self.accumulator[(x, y)].append((msg.r, msg.g, msg.b, msg.x_ring, msg.y_ring))

    def find_predef_rot(self, x_rviz, y_rviz):
        # print("x_rviz, y_rviz", x_rviz, y_rviz,"len",len(area_cylinder))
        kan = []
        for i in range(len(self.area_cylinder)):
            x1, y1, x2, y2 = self.area_cylinder[i]
            if min(x1, x2) < x_rviz < max(x1, x2) and min(y1, y2) < y_rviz < max(y1, y2):
                kan.append(i)
        if len(kan) != 1:
            # print("TO SE NEBI SMEL ZGODIT V find_predef_rot slepa tocka", len(kan))
            return None

        cylinder_point = [(0.07, -3.5), (1.7, -3.0), (1.2, -1.4), (-0.48, -2.1), (0.5, -0.27)]
        x_cp, y_cp = cylinder_point[kan[0]]
        ori = atan2(-y_cp + y_rviz, -x_cp + x_rviz)
        x_k = (x_cp-x_rviz)
        y_k = (y_cp-y_rviz)
        l = np.sqrt(x_k**2 + y_k**2)
        x_k = x_k / l
        y_k = y_k / l
        x_new = x_rviz + 0.5*x_k
        y_new = y_rviz + 0.5*y_k
        # print(x_k, y_k, x_new, y_new)
        return x_new, y_new, ori  # rvizkoordinate

    def find_color(self, r_point, g_point, b_point):
        barve_name = ["red", "green", "blue", "yellow"]
        index = int(np.argmax([r_point, g_point, b_point]))
        barve = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        if index == 2:
            print("[Cylinder] Cylinder color is -> ", barve_name[2])
            return barve[2][0], barve[2][1], barve[2][2], barve_name[2]
        elif abs(r_point-g_point) < 20:
            print("[Cylinder] Cylinder color is -> ", barve_name[3])
            return barve[3][0], barve[3][1], barve[3][2], barve_name[3]
        else:
            print("[Cylinder] Cylinder color is -> ", barve_name[index])
            return barve[index][0], barve[index][1], barve[index][2], barve_name[index]
            
    def send_marker(self, x, y, r, g, b):
        print("[Cylinder] sending marker")
        point_s = PointStamped()
        point_s.point.x = x
        point_s.point.y = y
        point_s.point.z = 0

        point_s.header.stamp = rospy.Time(0)

        pose = Pose()
        pose.position.x = x
        pose.position.y = y
        pose.position.z = 0
        marker = Marker()
        marker.header.stamp = rospy.Time(0)
        marker.header.frame_id = "map"
        marker.pose = pose
        marker.type = Marker.CYLINDER
        marker.action = Marker.ADD
        marker.frame_locked = False
        marker.lifetime = rospy.Time(1000)
        marker.id = self.markers_num
        marker.scale = Vector3(0.2, 0.2, 0.2)
        marker.color = ColorRGBA((1.0*r) / 255, (1.0*g) / 255, (1.0*b) / 255, 1)
        self.marker_array.markers.append(marker)
        self.markers_num += 1
        self.markers_pub.publish(self.marker_array)

    def map_callback(self, grid):
        size_x = grid.info.width
        size_y = grid.info.height
        if (size_x < 3) or (size_y < 3):
            print("[Cylinder] Map size is only x: %d,  y: %d . Not running map to image conversion", size_x, size_y)
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
    ring_Grabber = RingGrabber()
    dc = DetectCylinder()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Nekej")
