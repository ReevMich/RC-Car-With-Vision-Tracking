# file: test.py
# This is an example of how this module is used in a python script.
# For further understanding please visit the documentation.

import controller

me = controller.newController()
 
while(me.active):

    if(controller.getButtonDown(controller.BTN_PS)):
        print("PS BUTTON")
       
    if(controller.getAxisDown(controller.AXIS_R2)):
        print("R2=%d" % controller.getAxisValue(controller.AXIS_R2))

    if(controller.getAxisDown(controller.AXIS_L2)):
        print("L2=%d" % controller.getAxisValue(controller.AXIS_L2))

    if(controller.getAxisDown(controller.AXIS_LEFT_STICK_X)):
        print("LS_X=%d" % controller.getAxisValue(controller.AXIS_LEFT_STICK_X))

    if(controller.getAxisDown(controller.AXIS_LEFT_STICK_Y)):
        print("LS_Y=%d" % controller.getAxisValue(controller.AXIS_LEFT_STICK_Y))

    if(controller.getAxisDown(controller.AXIS_RIGHT_STICK_X)):
        print("RS_X=%d" % controller.getAxisValue(controller.AXIS_RIGHT_STICK_X))

    if(controller.getAxisDown(controller.AXIS_RIGHT_STICK_Y)):
        print("RS_Y=%d" % controller.getAxisValue(controller.AXIS_RIGHT_STICK_Y))

    if(controller.getButtonDown(controller.BTN_SQUARE)):
        print("SQUARE")

    if(controller.getButtonDown(controller.BTN_CIRCLE)):
        print("CIRCLE")
        
    if(controller.getButtonDown(controller.BTN_TRIANGLE)):
        print("TRIANGLE")

    if(controller.getButtonDown(controller.BTN_CROSS)):
        print("CROSS")

        
