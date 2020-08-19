#!/usr/bin/env python

import argparse
import sys
import time

import qi

import rospy

from pepper_motion_controll import PepperMotionControll
from pepper_image_input import  PepperImageInput
from pepper_virtual_motion_controll import VirtualPepperMotionControll

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number.")
    args = parser.parse_args()
    session = qi.Session()

    rospy.init_node("pepper_naoqi_py_node", anonymous=True)

    if (args.ip == "127.0.0.1"):
        VirtualPepperMotionControll()
    else:
        try:
            session.connect("tcp:://" + args.ip + ":" + str(args.port))
            PepperMotionControll(session)
            PepperImageInput(session)
        except RuntimeError:
            rospy.logerr("Can't connect to Naoqi at ip \"%s\" on port %n.\n"
                         "Please check your script arguments. Run with -h option for help.", args.ip, args.port)
            sys.exit(1)
        

    rospy.spin()