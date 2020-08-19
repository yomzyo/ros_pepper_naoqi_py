import rospy

from trajectory_msgs.msg._JointTrajectory import JointTrajectory

from qibullet import SimulationManager
from qibullet import PepperVirtual

class VirtualPepperMotionControll:
    def __init__(self):
        self.head_sub = rospy.Subscriber('/pepper_dcm/Head_controller/command', JointTrajectory, self.callback) 
        self.left_arm_sub = rospy.Subscriber('/pepper_dcm/LeftArm_controller/command', JointTrajectory, self.callback)       
        self.right_arm_sub = rospy.Subscriber('/pepper_dcm/RightArm_controller/command', JointTrajectory, self.callback)
        self.left_hand_sub = rospy.Subscriber('/pepper_dcm/LeftHand_controller/command', JointTrajectory, self.callback)
        self.right_hand_sub = rospy.Subscriber('/pepper_dcm/RightHand_controller/command', JointTrajectory, self.callback)

        self.simulation_manager = SimulationManager()
        self.client_id = self.simulation_manager.launchSimulation(gui=True)
        self.pepper = self.simulation_manager.spawnPepper(self.client_id, spawn_ground_plane=True)

    def callback(self, msg):
        print(msg.joint_names)
        print(list(msg.points[0].positions))
        self.pepper.setAngles(msg.joint_names, list(msg.points[0].positions))
    
    def __del__(self):
        self.simulation_manager.stopSimulation(self.client_id)
        self.motion_service.Destroy()