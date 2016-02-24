# file: test.py
# This is an example of how this module is used in a python script.
# For further understanding please visit the documentation.

import ControllerModule

controller = ControllerModule.newControllerOBJ()
 
while(controller.active):
    if(ControllerModule.getAxisDown(ControllerModule.AXIS_R2)):
        print("R2=%d" % ControllerModule.getAxisValue(ControllerModule.AXIS_R2))

    if(ControllerModule.getAxisDown(ControllerModule.AXIS_LEFT_STICK_X)):
        print("LS_X=%d" % ControllerModule.getAxisValue(ControllerModule.AXIS_LEFT_STICK_X))

    if(ControllerModule.getAxisDown(ControllerModule.AXIS_LEFT_STICK_Y)):
        print("LS_Y=%d" % ControllerModule.getAxisValue(ControllerModule.AXIS_LEFT_STICK_Y))
