from ax12_control.Ax12 import Ax12
import math
from Joint import Joint

# create Joint Objects
waist = Joint([1], 'waist')
shoulder = Joint([2, 3], 'shoulder')
elbow = Joint([4, 5], 'elbow')
wristPitch = Joint([6], 'wristPitch')
wristRoll = Joint([7], 'wristRoll')
gripper = Joint([8], 'gripper')

# all Joint objects
jointObjs = [waist, shoulder, elbow, wristPitch, wristRoll, gripper]

def config():
    """
    maps motor angles to conform with kinematic angles

    """
    waist.setMinMaxTheta(512)
    shoulder.setMinMaxTheta(751)
    elbow.setMinMaxTheta(761)
    wristPitch.setMinMaxTheta(512)
    wristRoll.setMinMaxTheta(512)
    gripper.setMinMaxTheta(512)

    setSpeedRaw(jointObjs,[100, 100, 100, 100, 100, 100])




# functions that apply to all joints
def getMotorPositions(jointObjs):
    
    for joint in jointObjs:

        jointName = joint.name
        position = joint.getMotorPosition()
        print(jointName + ': ' + str(position))


def getSpeedRaw(jointObjs):
    
    for joint in jointObjs:

        jointName = joint.name
        speedRaw = joint.getSpeedRaw()
        print(jointName + ': ' + str(speedRaw))


def setSpeedRaw(jointObjs, rawSpeeds):
    ''' Sets speed for all Joint Objects

    '''
    for joint, speed in zip(jointObjs, rawSpeeds):
        joint.setSpeedRaw(speed)

def enableTorque(jointObjs):
    ''' enable Torque for all Joint Objects

    '''
    for joint in jointObjs:
        joint.enableTorque()

def disableTorque(jointObjs):
    ''' disable Torque for all Joint Objects

    '''
    for joint in jointObjs:
        joint.disableTorque()



