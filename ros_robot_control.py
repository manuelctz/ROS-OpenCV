#!/urs/bin/env python

import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
import cv2

class RobotControl:

    def __init__(self):
        #create a new node
        rospy.init_node("Robot_Control")
        #Subscribe to the image_raw topic
        self.subs = rospy.Subscriber("/camera/image_raw",Image,self.callback)
        #Publish to the /cmd_vel topic
        self.publish = rospy.Publisher("/cmd_vel",Twist,queue_size=10)
        self.rate = rospy.Rate(10)
        self.vel = Twist()
        self.bridge = CvBridge()

    def callback(self,data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            cv2.imshow("show", cv_image)
            cv2.waitKey(0)
        except CvBridgeError as e:
            print(e)

        k = cv2.waitKey(0)

        if k == ord("i"):
            self.vel.linear.x = 0.2
            self.vel.angular.z = 0
        elif k == ord("k"):
            self.vel.linear.x = -0.2
            self.vel.angular.z = 0
        elif k == ord("j"):
            self.vel.linear.x = 0
            self.vel.angular.z = 0.3
        elif k == ord("l"):
            self.vel.linear.x = 0
            self.vel.angular.z = -0.3
        elif k == ord("q"):
            rospy.signal_shutdown("Shutting Down")
            cv2.destroyAllWindows()
        else:
            self.vel.linear.x = 0
            self.vel.angular.z = 0

        self.publish.publish(self.vel)
        self.rate.sleep()


if __name__ == "__main__":
    robot = RobotControl()
    try:
        if not rospy.is_shutdown():
            rospy.spin()
    except rospy.ROSInterruptException as e:
        print(e)
