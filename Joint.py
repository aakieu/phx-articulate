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


    def getMotorPositions(self):
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

    def getSpeedRaw(self): 
        """ Returns a list of raw motor speed values for each joint

        """ 
        return [motorObject.get_moving_speed() for motorObject in self.motorObjects]

    def setSpeedRaw(self, speed):
        """  Sets the raw motor speed value(s) for each joint object

        """
        for motorObject in self.motorObjects:
            motorObject.set_moving_speed(speed)


