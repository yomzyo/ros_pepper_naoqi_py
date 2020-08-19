import qi
import rospy

import cv2 as cv

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class PepperImageInput:
    def __init__(self, session):
        self.session = session
        self.video_service = session.service("ALVideoDevice")
        self.timer_pub = rospy.Timer(rospy.Duration(0.01666), self.timer_pub_callback)

        self.image_pub = rospy.Publisher('/pepper_image/camera', Image)
        self.bridge = CvBridge()

        self._imgClient = ""
        self._registerImageClient()
        self._cvImage = None

    def _registerImageClient(self):
        resolution = vision_definitions.kVGA
        colortSpace = vision_definitions.kRGBColorSpace
        self._imgClient = self.video_service.subscribe("_client", resolution, colortSpace, 5)
        self.video_service.setParam(vision_definitions.kCameraSelectID, 0)

    def _unregisterImageClient(self):
        if self._imgClient != "":
            self.video_service.unsubscribe(self._imgClient)

    def _updateImage(self):
        alImage = self.video_service.getImageRemote(self._imgClient)
        if (alImage == None):
            rospy.logerr('Cannot capture image')
        elif (alImage[6] == None):
            rospy.logerr('No image data string')
        else:
            width = alImage[0]
            height = alImage[1]
            self._cvImage = Image.frombytes('RGB', (width, height), COLOR_RGB2BGRA)

    def timer_pub_callback(self, event):
        self._updateImage()
        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(_cvImage, "bgr8"))
        except CvBridgeError as e:
            rospy.logerr(e)

    def __del__(self):
        self._unregisterImageClient()
    

