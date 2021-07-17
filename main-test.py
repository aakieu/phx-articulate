from ax12_control.Ax12 import Ax12
import math
from Joint import Joint
import phx
from phx import *
import kinematics as kin 

CONNECT = True
WINDOWS = False

# hardware testing 
if CONNECT:
    if WINDOWS: Ax12.DEVICENAME = 'COM3'
    Ax12.connect()
    phx.config()


    # Ax12.disconnect()
