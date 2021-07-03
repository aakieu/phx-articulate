from ax12_control.Ax12 import Ax12
import math
import phx
from Joint import Joint

# create Joint Objects
waist = Joint([1], 'Waist')
shoulder = Joint([2, 3], 'Shoulder')
elbow = Joint([4, 5], 'Elbow')
wristPitch = Joint([6], 'WristPitch')
gripper = Joint([7], 'Gripper')

# all Joint objects
jointObjs = [waist, shoulder, elbow, wristPitch, gripper]

CONNECT = True
WINDOWS = False

# hardware testing 
if CONNECT:
    if WINDOWS: Ax12.DEVICENAME = 'COM3'
    Ax12.connect()
    setSpeedRaw(jointObjs,[100, 100, 100, 100, 100])

    # map angles
    waist.setMinMaxTheta(512)
    shoulder.setMinMaxTheta(761)
    # elbow.setMinMaxTheta()
    # wristPitch.setMinMaxTheta()
    # wristRoll.setMinMaxTheta()

    # hardware test
    #shoulder.setPositionAngle()


    # getMotorPositions(jointObjs)
    # Ax12.disconnect()