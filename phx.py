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
allJoints = [waist, shoulder, elbow, wristPitch, wristRoll, gripper]

# poses 

initPose = [0, 90, -90, 0, 0, 0]
sleepPose = [1, 159, -159, 16, 1, 0]

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

    setRawSpeeds(allJoints,[100, 100, 100, 100, 100, 100])

# functions that apply to all joints
def getRawPositions(jointObjs):
    
    for joint in jointObjs:

        jointName = joint.name
        position = joint.getRawPosition()
        print(jointName + ': ' + str(position))


def getRawSpeeds(jointObjs):
    
    for joint in jointObjs:

        jointName = joint.name
        speedRaw = joint.getRawSpeed()
        print(jointName + ': ' + str(speedRaw))


def setRawSpeeds(jointObjs, rawSpeeds):
    ''' Sets speed for all Joint Objects

    '''
    for joint, speed in zip(jointObjs, rawSpeeds):
        joint.setRawSpeed(speed)

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

def getAngles(jointObjs):

    return [joint.getAngle() for joint in jointObjs]

    # for joint in jointObjs:

    #     jointName = joint.name
    #     kinTheta = joint.getAngle()
    #     print(jointName + ': ' + str(position))

def setAngles(jointObjs, angles):
    for joint, angle in zip(jointObjs, angles):
        joint.setAngle(angle)



def setPose(poseName):
    setAngles(allJoints,poseName)