from ax12_control.Ax12 import Ax12
import math
from Joint import Joint

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

