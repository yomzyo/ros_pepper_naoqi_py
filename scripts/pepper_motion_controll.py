import qi
import rospy

from trajectory_msgs.msg._JointTrajectory import JointTrajectory

class PepperMotionControll:
    def __init__(self, session):
        self.session = session
        self.motion_service = session.service("ALMotion")
        self.motion_service.setStiffness("Body", 1.0)

        self.head_sub = rospy.Subscriber('/pepper_dcm/Head_controller/command', JointTrajectory, self.callback) 
        self.left_arm_sub = rospy.Subscriber('/pepper_dcm/LeftArm_controller/command', JointTrajectory, self.callback)       
        self.right_arm_sub = rospy.Subscriber('/pepper_dcm/RightArm_controller/command', JointTrajectory, self.callback)
        self.left_hand_sub = rospy.Subscriber('/pepper_dcm/LeftHand_controller/command', JointTrajectory, self.callback)
        self.right_hand_sub = rospy.Subscriber('/pepper_dcm/RightHand_controller/command', JointTrajectory, self.callback)

    def callback(self, msg):
        self.motion_service.SetAngles(msg.joint_names, msg.points[0].positions, 0.8)
    
    def __del__(self):
        self.motion_service.Destroy()