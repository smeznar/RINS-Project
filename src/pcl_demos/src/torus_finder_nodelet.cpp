#include <iostream>
#include <ros/ros.h>
#include <math.h>
#include <visualization_msgs/Marker.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/ModelCoefficients.h>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/filters/passthrough.h>
#include <pcl/features/normal_3d.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/segmentation/sac_segmentation.h>
#include "pcl/point_cloud.h"
#include "tf2_ros/transform_listener.h"
#include "tf2_geometry_msgs/tf2_geometry_msgs.h"
#include "geometry_msgs/PointStamped.h"
#include "pcl_demos/RingPose.h"
#include <algorithm>

#include <nav_msgs/GetMap.h>
#include <geometry_msgs/Quaternion.h>
#include <geometry_msgs/PoseStamped.h>
#include <tf2/transform_datatypes.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>


ros::Publisher pubx;
ros::Publisher puby;
ros::Publisher pubm;
ros::Publisher publisher;
tf2_ros::Buffer tf2_buffer;
using namespace std;
using namespace cv;

typedef pcl::PointXYZRGB PointT;
//////////////////////7
Mat cv_map;
float map_resolution = 0;
geometry_msgs::TransformStamped map_transform;
int size_x;
int size_y;

/// Color
int red;
int green;
int blue;
int color_count;

int x_wall[8] = {244, 240, 253, 258, 255, 265, 267, 276};
int y_wall[8] = {28, 40, 45, 71, 81, 86, 76, 57};


struct RGB {
	int r,g,b;
};


bool compere_rgb_b(const RGB a, const RGB b)
{
	return a.b > b.b;
}
bool compere_rgb_r(const RGB a, const RGB b)
{
	return a.r > b.r;
}
bool compere_rgb_g(const RGB a, const RGB b)
{
	return a.g > b.g;
}

//Arg je narjen ce ga bomo magar kdaj rabl
float closestWall(int map_x, int map_y) {
    float min_distance = 10000;
    int arg = -1;
    for (int i = 0; i < 8; i++) {
        float dx = map_x - x_wall[i];
        float dy = map_y - y_wall[i];
        float dist = sqrt(dx * dx + dy * dy);
        if (dist < min_distance) {
            min_distance = dist;
            arg = i;
        }
    }
    return min_distance;
}

void mapCallback(const nav_msgs::OccupancyGridConstPtr &msg_map) {
    size_x = msg_map->info.width;
    size_y = msg_map->info.height;

    if ((size_x < 3) || (size_y < 3)) {
        ROS_INFO("Map size is only x: %d,  y: %d . Not running map to image conversion", size_x, size_y);
        return;
    }
    // resize cv image if it doesn't have the same dimensions as the map
    if ((cv_map.rows != size_y) && (cv_map.cols != size_x)) {
        cv_map = cv::Mat(size_y, size_x, CV_8U);
    }


    map_resolution = msg_map->info.resolution;
    map_transform.transform.translation.x = msg_map->info.origin.position.x;
    map_transform.transform.translation.y = msg_map->info.origin.position.y;
    map_transform.transform.translation.z = msg_map->info.origin.position.z;

    map_transform.transform.rotation = msg_map->info.origin.orientation;

    //tf2::poseMsgToTF(msg_map->info.origin, map_transform);

    const std::vector <int8_t> &map_msg_data(msg_map->data);

    unsigned char *cv_map_data = (unsigned char *) cv_map.data;

    //We have to flip around the y axis, y for image starts at the top and y for map at the bottom
    int size_y_rev = size_y - 1;

    for (int y = size_y_rev; y >= 0; --y) {

        int idx_map_y = size_x * (size_y - y);
        int idx_img_y = size_x * y;

        for (int x = 0; x < size_x; ++x) {

            int idx = idx_img_y + x;

            switch (map_msg_data[idx_map_y + x]) {
                case -1:
                    cv_map_data[idx] = 127;
                    break;

                case 0:
                    cv_map_data[idx] = 255;
                    break;

                case 100:
                    cv_map_data[idx] = 0;
                    break;
            }
        }
    }

}

double CalcMHWScore(vector<int> scores)
{
    size_t size = scores.size();

    if (size == 0)
    {
        return 0;  // Undefined, really.
    }
    else
    {
        sort(scores.begin(), scores.end());
        if (size % 2 == 0)
        {
            return (scores[size / 2 - 1] + scores[size / 2]) / 2;
        }
        else
        {
            return scores[size / 2];
        }
    }
}

bool nasa_f(const PointT a ,const PointT b )
	{
		uint32_t rgb_a = ((uint32_t)a.rgb);
		int b_a = (int)((rgb_a)       & 0x0000ff);
		uint32_t rgb_b = ((uint32_t)b.rgb);
		int b_b = (int)((rgb_b)       & 0x0000ff);
		return b_a > b_b;
	} 

pcl::PCLPointCloud2 projekcijaTockNaTla(const pcl::PointCloud<PointT>::Ptr cloud, ros::Time time_rec) {
    //std::cerr << "Ring points before has: " << cloud->points.size() << " data points." << std::endl;
    geometry_msgs::TransformStamped tss;
    pcl::PointCloud <PointT> pointCloud;
    try {
        tss = tf2_buffer.lookupTransform("map", "camera_rgb_optical_frame", time_rec, ros::Duration(1));
    }
    catch (tf2::TransformException ex) {
        ROS_ERROR("%s", ex.what());
        ros::Duration(1.0).sleep();
        pcl::PCLPointCloud2 outcloud_cylinder;
        return outcloud_cylinder;
    }

    pointCloud.header = cloud->header;
    unsigned char *cv_map_data = (unsigned char *) cv_map.data;
    red = 0;
    green = 0;
    blue = 0;
    color_count = 0;

    vector<int> vec_r;
    vector<int> vec_g;
    vector<int> vec_b;

    for (int i = 0; i < cloud->points.size(); i++) {
        float x = cloud->points[i].x;
        float y = cloud->points[i].y;
        float z = cloud->points[i].z;
        //transformiraj v map
        //TODO X,Y,Z so lah zmensani

        geometry_msgs::PointStamped point_camera;
        geometry_msgs::PointStamped point_map;

        point_camera.point.x = x;
        point_camera.point.y = y;
        point_camera.point.z = z;


        tf2::doTransform(point_camera, point_map, tss);




        int map_x = (int) ((point_map.point.x - map_transform.transform.translation.x) / map_resolution);
        int map_y = size_y - (int) ((point_map.point.y - map_transform.transform.translation.y) / map_resolution);
        //TODO najdmo pravo razdaljo je razdalja v pikslih gleda sam da je tocka blizu ene od skatel

        if (closestWall(map_x, map_y) > 12) {
            continue;
        }

        int index = map_y * size_x + map_x;
        bool ring = true;
        int r = 2;
        for (int xx = map_x - r; xx <= map_x + r; xx++) {
            for (int yy = map_y - r; yy <= map_y + r; yy++) {
                int index_tmp = yy * size_x + xx;
                ring = ring && (cv_map_data[index_tmp] == 255);
            }
        }
        //rgb->hsv

        if (ring) {
            // maybe filter by color also?
            uint32_t rgb = * reinterpret_cast<int*>(&(cloud->points[i]).rgb);
            int r = (int) ((rgb >> 16) & 0x0000ff);
            int g = (int) ((rgb >> 8)  & 0x0000ff);
            int b = (int)((rgb)       & 0x0000ff);
            if ((ring) //red
                || (ring) // green
                || (ring) // blue
                || (ring)){ // black
                //red += r;
                //green += g;
                //blue += b;
                //color_count++;
                pointCloud.push_back(cloud->points[i]);
                //vec_r.push_back(r);
                //vec_g.push_back(g);
                //vec_b.push_back(b);
            }
        }


    }

    //std::cerr << "cez "<< blue << std::endl;

    // Maybe do in the other function or a global variables
    /*
    if (color_count != 0) {
        red = (int) (red / color_count);
        green = (int) (green / color_count);
        blue = (int) (blue / color_count);
        //std::cerr << "red: " << red << ", green: " << green << ", blue: " << blue << std::endl;
    }
     */
    //cloud->points = pointCloud.points;
    //std::cerr << "Ring points has: " << pointCloud.points.size() << " data points." << std::endl;
    pcl::PCLPointCloud2 outcloud_cylinder;
    pcl::toPCLPointCloud2(pointCloud, outcloud_cylinder);
    /*
    red = CalcMHWScore(vec_r);
    green = CalcMHWScore(vec_g);
    blue = CalcMHWScore(vec_b);
    std::cerr << "red: " << red << ", green: " << green << ", blue: " << blue << std::endl;
    */
    //pubx.publish(outcloud_cylinder);
    //Mat img(Size(size_x,size_y),CV_8U,cv_map_data);
    //namedWindow("Map");
    //imshow("Map", img);
    //imshow("Map", cv_map);
    //waitKey(30);
    return outcloud_cylinder;
}

void cloud_cb(const pcl::PCLPointCloud2ConstPtr &cloud_blob) {
    // All the objects needed

    ros::Time time_rec;
    time_rec = pcl_conversions::fromPCL(cloud_blob->header.stamp);
    pcl::PassThrough <PointT> pass;
    pcl::NormalEstimation <PointT, pcl::Normal> ne;
    pcl::SACSegmentationFromNormals <PointT, pcl::Normal> seg;
    pcl::PCDWriter writer;
    pcl::ExtractIndices <PointT> extract;
    pcl::ExtractIndices <pcl::Normal> extract_normals;
    pcl::search::KdTree<PointT>::Ptr tree(new pcl::search::KdTree<PointT>());
    Eigen::Vector4f centroid;

    // Datasets
    pcl::PointCloud<PointT>::Ptr cloud(new pcl::PointCloud <PointT>);
    pcl::PointCloud<PointT>::Ptr cloud_filtered(new pcl::PointCloud <PointT>);
    pcl::PointCloud<pcl::Normal>::Ptr cloud_normals(new pcl::PointCloud <pcl::Normal>);
    pcl::PointCloud<PointT>::Ptr cloud_filtered2(new pcl::PointCloud <PointT>);
    pcl::PointCloud<pcl::Normal>::Ptr cloud_normals2(new pcl::PointCloud <pcl::Normal>);
    pcl::ModelCoefficients::Ptr coefficients_plane(new pcl::ModelCoefficients), coefficients_cylinder(
            new pcl::ModelCoefficients);
    pcl::PointIndices::Ptr inliers_plane(new pcl::PointIndices), inliers_cylinder(new pcl::PointIndices);

    // Read in the cloud data
    pcl::fromPCLPointCloud2(*cloud_blob, *cloud);
    //std::cerr << "PointCloud has: " << cloud->points.size() << " data points." << std::endl;

    // Build a passthrough filter to remove spurious NaNs
    pass.setInputCloud(cloud);
    pass.setFilterFieldName("z");
    pass.setFilterLimits(0, 2);
    pass.filter(*cloud_filtered);
    //std::cerr << "PointCloud after filtering has: " << cloud_filtered->points.size () << " data points." << std::endl;


    // Build a passthrough filter to remove spurious NaNs
    pass.setInputCloud(cloud_filtered);
    pass.setFilterFieldName("y"); //TODO magar je y
    pass.setFilterLimits(-0.5, -0.1);
    //pass.setFilterLimits (-1, 1);
    pass.filter(*cloud_filtered);
    //std::cerr << "PointCloud after filtering has: " << cloud_filtered->points.size () << " data points." << std::endl;



    bool work = true;
    for (int i = 0; i < 5; i++) {

        // Estimate point normals
        ne.setSearchMethod(tree);
        ne.setInputCloud(cloud_filtered);
        ne.setKSearch(50);
        ne.compute(*cloud_normals);

        // Create the segmentation object for the planar model and set all the parameters
        seg.setOptimizeCoefficients(true);
        seg.setModelType(pcl::SACMODEL_NORMAL_PLANE);
        seg.setNormalDistanceWeight(0.1);
        seg.setMethodType(pcl::SAC_RANSAC);
        seg.setMaxIterations(1000);
        seg.setDistanceThreshold(0.03);
        seg.setInputCloud(cloud_filtered);
        seg.setInputNormals(cloud_normals);
        // Obtain the plane inliers and coefficients
        seg.segment(*inliers_plane, *coefficients_plane);
        //std::cerr << "Plane coefficients: " << *coefficients_plane << std::endl;

        // Extract the planar inliers from the input cloud
        extract.setInputCloud(cloud_filtered);
        extract.setIndices(inliers_plane);
        extract.setNegative(false);



        // Write the planar inliers to disk
        pcl::PointCloud<PointT>::Ptr cloud_plane(new pcl::PointCloud<PointT>());
        extract.filter(*cloud_plane);
        //std::cerr << "PointCloud representing the planar component: " << cloud_plane->points.size () << " data points." << std::endl;


        // Remove the planar inliers, extract the rest
        extract.setNegative(true);
        extract.filter(*cloud_filtered2);
        extract_normals.setNegative(true);
        extract_normals.setInputCloud(cloud_normals);
        extract_normals.setIndices(inliers_plane);
        extract_normals.filter(*cloud_normals2);

        pcl::PCLPointCloud2 outcloud_torus;
        pcl::toPCLPointCloud2(*cloud_filtered2, outcloud_torus);
        cloud_filtered = cloud_filtered2;
        //TODO
        if (cloud_filtered->points.size() < 20000) break;
        //pubx.publish (outcloud_torus);
    }
    pcl::PCLPointCloud2 returned_cloud;
    returned_cloud = projekcijaTockNaTla(cloud_filtered, time_rec);
    pcl::PointCloud<PointT>::Ptr cloud_filtered3(new pcl::PointCloud <PointT>);
    pcl::fromPCLPointCloud2(returned_cloud, *cloud_filtered3);
    pcl::PointCloud<pcl::Normal>::Ptr cloud_normals3(new pcl::PointCloud <pcl::Normal>);
    // Create the segmentation object for cylinder segmentation and set all the parameters
    seg.setOptimizeCoefficients(true);
    //seg.setModelType (pcl::SACMODEL_CYLINDER);
    ne.setSearchMethod(tree);
    ne.setInputCloud(cloud_filtered3);
    ne.setKSearch(50);
    ne.compute(*cloud_normals3);

    seg.setModelType(pcl::SACMODEL_CIRCLE3D);//!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
    seg.setMethodType(pcl::SAC_RANSAC);
    seg.setNormalDistanceWeight(0.1);
    seg.setMaxIterations(1000);
    seg.setDistanceThreshold(0.05);
    seg.setRadiusLimits(0.06, 0.2);
    seg.setInputCloud(cloud_filtered3);
    seg.setInputNormals(cloud_normals3);

    // Obtain the cylinder inliers and coefficients
    seg.segment(*inliers_cylinder, *coefficients_cylinder);
    //std::cerr << "Cylinder coefficients: " << *coefficients_cylinder << std::endl;

    // Write the cylinder inliers to disk
    extract.setInputCloud(cloud_filtered3);
    extract.setIndices(inliers_cylinder);
    extract.setNegative(false);
    pcl::PointCloud<PointT>::Ptr cloud_cylinder(new pcl::PointCloud<PointT>());
    extract.filter(*cloud_cylinder);
    if (cloud_cylinder->points.empty())
        std::cerr << "Can't find the cylindrical component." << std::endl;
    else {
        /*
        std::cerr << "PointCloud representing the cylindrical component: " << cloud_cylinder->points.size()
                  << " data points." << std::endl;
        */
        pcl::compute3DCentroid(*cloud_cylinder, centroid);
        /*
        std::cerr << "centroid of the cylindrical component: " << centroid[0] << " " << centroid[1] << " "
                  << centroid[2] << " " << centroid[3] << std::endl;
        */
        //Create a point in the "camera_rgb_optical_frame"
        geometry_msgs::PointStamped point_camera;
        geometry_msgs::PointStamped point_map;
        visualization_msgs::Marker marker;
        geometry_msgs::TransformStamped tss;

        point_camera.header.frame_id = "camera_rgb_optical_frame";
        point_camera.header.stamp = ros::Time::now();

        point_map.header.frame_id = "map";
        point_map.header.stamp = ros::Time::now();

        point_camera.point.x = centroid[0];
        point_camera.point.y = centroid[1];
        point_camera.point.z = centroid[2];

        try {
            //std::cerr << time_rec << std::endl;
            tss = tf2_buffer.lookupTransform("map", "camera_rgb_optical_frame", time_rec, ros::Duration(1));
            //tf2_buffer.transform(point_camera, point_map, "map", ros::Duration(2));
        }
        catch (tf2::TransformException &ex) {
            ROS_WARN("Transform warning: %s\n", ex.what());
        }

        //std::cerr << tss ;

        tf2::doTransform(point_camera, point_map, tss);
        /*
        std::cerr << "point_camera: " << point_camera.point.x << " " << point_camera.point.y << " "
                  << point_camera.point.z << std::endl;

        std::cerr << "point_map: " << point_map.point.x << " " << point_map.point.y << " " << point_map.point.z
                  << std::endl;

        marker.header.frame_id = "map";
        marker.header.stamp = ros::Time::now();

        marker.ns = "cylinder";
        marker.id = 0;

        marker.type = visualization_msgs::Marker::CYLINDER;
        marker.action = visualization_msgs::Marker::ADD;

        marker.pose.position.x = point_map.point.x;
        marker.pose.position.y = point_map.point.y;
        marker.pose.position.z = point_map.point.z;
        marker.pose.orientation.x = 0.0;
        marker.pose.orientation.y = 0.0;
        marker.pose.orientation.z = 0.0;
        marker.pose.orientation.w = 1.0;

        marker.scale.x = 0.1;
        marker.scale.y = 0.1;
        marker.scale.z = 0.1;

        marker.color.r = 0.0f;
        marker.color.g = 1.0f;
        marker.color.b = 0.0f;
        marker.color.a = 1.0f;

        marker.lifetime = ros::Duration();
//
        pubm.publish(marker);
*/
        pcl::PCLPointCloud2 outcloud_cylinder;
        pcl::toPCLPointCloud2(*cloud_cylinder, outcloud_cylinder);
        puby.publish(outcloud_cylinder);
        //pubx.publish(outcloud_cylinder);
	double min_y = 10000;
	double max_y = -10000;	
	for(int i = 0; i < cloud_cylinder->points.size(); i++){
		double p = cloud_cylinder->points[i].y;
		//double p2 = cloud_cylinder->points[i].x;
		//double p3 = cloud_cylinder->points[i].z;
		//std::cerr << "tocka y " << p<< "tocka x " << p2<< "tocka z " << p3 << std::endl;
		if(p <min_y) min_y = p;
		if(p > max_y) max_y = p;
	}
	double premer = max_y - min_y;
	double meja = (max_y + min_y)/2;
	vector<int> vec_r;
    	vector<int> vec_g;
    	vector<int> vec_b;
	vector<RGB> tocke;
	int num_r = 0;
	int num_g = 0;
	int num_b = 0;
	int sum_r = 0;
	int sum_g = 0;
	int sum_b = 0;
	for(int i = 0; i < cloud_cylinder->points.size(); i++){
		double p = cloud_cylinder->points[i].y;
		if (p > meja){
			uint32_t rgb = * reinterpret_cast<int*>(&(cloud_cylinder->points[i]).rgb);
            		uint8_t r =  ((rgb >> 16) & 0x0000ff);
            		uint8_t g =  (((rgb >> 8)  & 0x0000ff));
            		uint8_t b = ((rgb)       & 0x0000ff);
			sum_r += r;
			sum_g += g;
			sum_b += b;
			/*
			int r = (cloud->points[i]).r;
			int g = (cloud->points[i]).g;
			int b = (cloud->points[i]).b;
			*/			
			printf("%d %d %d\n", r,g,b);
//			std::cerr << "r: " << r<< " g:" << g << " b:"<<b <<std::endl;
			//vec_r.push_back(r);
                	//vec_g.push_back(g);
                	//vec_b.push_back(b);
					//RGB tocka;
					//tocka.r = r;
					//tocka.g = g;
					//tocka.b = b;
					//tocke.push_back(tocka);

					if (r >= b && r >= g){
						num_r++;
					}
					if (g >= r && g >= b){
						num_g++;
					}
					if (b >= r && b >= g){
						num_b++;
					}

		}
	}
	sum_r =sum_r /cloud_cylinder->points.size();
	sum_g =sum_g /cloud_cylinder->points.size();
	sum_b =sum_b /cloud_cylinder->points.size();
/*
	std::cerr << "mediane"<<std::endl;
	std::sort(tocke.begin(),tocke.end(),compere_rgb_b);
	RGB median = tocke[tocke.size()/2];

	std::cerr << "r: " << median.r<< " g:" << median.g << " b:"<<median.b <<std::endl;
	std::sort(tocke.begin(),tocke.end(),compere_rgb_r);

	median = tocke[tocke.size()/2];
	std::cerr << "r: " << median.r<< " g:" << median.g << " b:"<<median.b <<std::endl;
	std::sort(tocke.begin(),tocke.end(),compere_rgb_g);
	median = tocke[tocke.size()/2];
	std::cerr << "r: " << median.r<< " g:" << median.g << " b:"<<median.b <<std::endl;

*/
	std::cerr << "num_r: " << num_r<< " num_g:" << num_g << " num_b:"<< num_b <<std::endl;	
	std::cerr << "sum_r: " << sum_r<< " sum_g:" << sum_g << " sum_b:"<< sum_b <<std::endl;	
	//red = CalcMHWScore(vec_r);
    	//green = CalcMHWScore(vec_g);
    	//blue = CalcMHWScore(vec_b);
	std::cerr << "Premer " << premer << std::endl;
        pcl_demos::RingPose msg;
        msg.x_ring = point_map.point.x;
        msg.y_ring = point_map.point.y;
        //msg.r = coefficients_cylinder->values[3]; //TODO PREVER TA PAR
        msg.r = num_r;
        msg.g = num_g;
        msg.b = num_b;
        publisher.publish(msg);
    }


}






/////////////////////7

int main(int argc, char **argv) {
    // Initialize ROS
    ros::init(argc, argv, "cylinder_segment");
    ros::NodeHandle nh;

    // For transforming between coordinate frames
    tf2_ros::TransformListener tf2_listener(tf2_buffer);

    // Create a ROS subscriber for the input point cloud
    //ros::Subscriber sub = nh.subscribe ("input", 1, cloud_cb);
    ros::Subscriber sub = nh.subscribe("input", 1, cloud_cb);
    ros::Subscriber sub_map = nh.subscribe("map", 10, &mapCallback);
    publisher = nh.advertise<pcl_demos::RingPose>("grab_3d_ring", 1000);
    // Create a ROS publisher for the output point cloud
    pubx = nh.advertise<pcl::PCLPointCloud2>("torus", 1);
    puby = nh.advertise<pcl::PCLPointCloud2>("cylinder", 1);

    pubm = nh.advertise<visualization_msgs::Marker>("detected_cylinder", 1);

    // Spin
    ros::spin();
}
