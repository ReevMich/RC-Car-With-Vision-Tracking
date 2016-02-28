# file: test.py
# This is an example of how this module is used in a python script.
# For further understanding please visit the documentation.

import ControllerModule

controller = ControllerModule.newControllerOBJ()
 
while(controller.active):
    if(ControllerModule.getAxisDown(ControllerModule.AXIS_R2)):
        print("R2=%d" % ControllerModule.getAxisValue(ControllerModule.AXIS_R2))

    if(ControllerModule.getAxisDown(ControllerModule.AXIS_L2)):
        print("L2=%d" % ControllerModule.getAxisValue(ControllerModule.AXIS_L2))

    if(ControllerModule.getAxisDown(ControllerModule.AXIS_LEFT_STICK_X)):
        print("LS_X=%d" % ControllerModule.getAxisValue(ControllerModule.AXIS_LEFT_STICK_X))

    if(ControllerModule.getAxisDown(ControllerModule.AXIS_LEFT_STICK_Y)):
        print("LS_Y=%d" % ControllerModule.getAxisValue(ControllerModule.AXIS_LEFT_STICK_Y))

    if(ControllerModule.getAxisDown(ControllerModule.AXIS_RIGHT_STICK_X)):
        print("RS_X=%d" % ControllerModule.getAxisValue(ControllerModule.AXIS_RIGHT_STICK_X))

    if(ControllerModule.getAxisDown(ControllerModule.AXIS_RIGHT_STICK_Y)):
        print("RS_Y=%d" % ControllerModule.getAxisValue(ControllerModule.AXIS_RIGHT_STICK_Y))

    if(ControllerModule.getKeyDown(ControllerModule.BTN_SQUARE)):
        print("SQUARE")

    if(ControllerModule.getKeyDown(ControllerModule.BTN_CIRCLE)):
        print("CIRCLE")
        
    if(ControllerModule.getKeyDown(ControllerModule.BTN_TRIANGLE)):
        print("TRIANGLE")

    if(ControllerModule.getKeyDown(ControllerModule.BTN_CROSS)):
        print("CROSS")

        
