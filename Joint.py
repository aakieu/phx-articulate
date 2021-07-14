import math
from ax12_control.Ax12 import Ax12

class Joint():
    """ Class for each robot joint"""

    def __init__(self, motorIds,name):
        """Initialize motor with id"""
        self.motorObjects = [Ax12(motorID) for motorID in motorIds]
        self.name = name

        if len(self.motorObjects) == 1:
            self.multiple = False
        else:
            self.multiple = True


    def getRawPosition(self):
        """ Returns a list of raw motor position values for each joint

        """ 
        return [motorObject.get_present_position() for motorObject in self.motorObjects]
           
    def setPositionRaw(self, position):
        """  Sets the raw motor position value(s) for each joint

        """
        if self.multiple:
            self.motorObjects[0].set_goal_position(position)
            self.motorObjects[1].set_goal_position(1023 - position)
        else:
            self.motorObjects[0].set_goal_position(position)

    def getRawSpeed(self): 
        """ Returns a list of raw motor speed values for each joint

        """ 
        return [motorObject.get_moving_speed() for motorObject in self.motorObjects]

    def setRawSpeed(self, speed):
        """  Sets the raw motor speed value(s) for each joint object

        """
        for motorObject in self.motorObjects:
            motorObject.set_moving_speed(speed)

    def enableTorque(self):
        for motorObject in self.motorObjects:
            motorObject.enable_torque() 

    def disableTorque(self):
        for motorObject in self.motorObjects:
            motorObject.disable_torque()
            
    def setMinMaxTheta(self, rawZeroAngle):
        """
        rawZeroAngle - the raw motor position value where position of joint is 0 degrees on kinematic diagram

        """
        if self.name == 'shoulder':
            print('inverted motor joint')
            self.thetaMin = math.ceil(0 - Ax12.raw2deg(1023 - rawZeroAngle))
            self.thetaMax = math.ceil(Ax12.raw2deg(rawZeroAngle))

        else:
            self.thetaMin = math.ceil(0 - Ax12.raw2deg(rawZeroAngle))
            self.thetaMax = math.ceil(Ax12.raw2deg(1023-rawZeroAngle))

        print(self.name + " thetaMin: " + str(self.thetaMin))
        print(self.name + " thetaMax: " + str(self.thetaMax))


    def degToRawPos(self, angleIn):
        """ Converts angle (based on kinematic diagram) into raw motor positions 
        thetaMin/Max is set using setMinMaxTheta()

        """
        if self.name == 'shoulder' :
            rawPos = math.ceil(self.mapLinear(angleIn, self.thetaMax, self.thetaMin, 0, 1023))
        else:
            rawPos = math.ceil(self.mapLinear(angleIn, self.thetaMin, self.thetaMax, 0, 1023))

        return rawPos

    def setAngle(self, angle):
        """ Writes input angle (from kinematic diagram) to motor
        """
        self.setPositionRaw(self.degToRawPos(angle))

    def getAngle(self):
        """ Returns kinematic angle of Joint
        """

        rawPos = self.getRawPosition()[0]

        if self.name == 'shoulder' :
            kinTheta = math.ceil(self.mapLinear(rawPos,0,1023, self.thetaMax, self.thetaMin))
        else:
            kinTheta = math.ceil(self.mapLinear(rawPos,0,1023, self.thetaMin, self.thetaMax))

        return kinTheta


    @staticmethod
    def mapLinear(x_in, x_min, x_max, y_min, y_max):
        """Linearly maps x to y; returns corresponding y value

        """
        m = ((y_max - y_min) / (x_max - x_min))
        y_out = m * (x_in - x_min) + y_min
        return y_out



