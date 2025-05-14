#!/usr/bin/env python3
"""
RGBdata make: hhs
Modified for ROS 2 Humble
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import cv2
from cv_bridge import CvBridge
import numpy as np

class ColorLineFollower(Node):
    def __init__(self):
        super().__init__('color_line_follower')
        
        self.subscription = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.camera_callback,
            10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.bridge = CvBridge()
        self.twist = Twist()
        self.lower_color = np.array([20, 100, 100])
        self.upper_color = np.array([30, 255, 255])

    def camera_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_color, self.upper_color)
        
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=2)
        
        m = cv2.moments(mask)
        if m['m00'] > 0:
            cx = int(m['m10'] / m['m00'])
            cy = int(m['m01'] / m['m00'])
            
            x, y, w, h = cv2.boundingRect(mask)
            cv2.rectangle(image, (x,y), ((x+w),(y+h)), (250,140,150), 3)
            cv2.circle(image, (cx,cy), 3, (255,0,255), 2)
            
            error = cx - image.shape[1] / 2
            
            self.twist.linear.x = 0.5
            self.twist.angular.z = -(error / 100)
            self.publisher.publish(self.twist)
        
        cv2.imshow("Output", image)
        cv2.imshow("masked", mask)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    follower = ColorLineFollower()
    rclpy.spin(follower)
    follower.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
