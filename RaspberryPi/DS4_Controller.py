#!/usr/bin/python

from DS4Controller.src import controller
from time import sleep


def main(out_arduino_wheel_speed_pipe, out_run_prog_pipe):

    out_wheels_pipe, _ = out_arduino_wheel_speed_pipe
    out_run_prog_pipe, _ = out_run_prog_pipe

    # init ds4 controller
    ds4_controller = controller.newController()

    # lets us know when to exit to program
    square_pressed = False
    reverse = False

    # Speed of the wheels
    prev_left = 0.0
    prev_right = 0.0
    while ds4_controller.active and square_pressed is False:

        if controller.getButtonDown(controller.BTN_SQUARE):
            reverse = True
            print "Reverse: True"
        else:
            reverse = False

        try:
            if controller.getAxisDown(controller.AXIS_R2):
                right_wheels = float(
                    controller.getAxisValue(controller.AXIS_R2))
                print right_wheels
            else:
                right_wheels = 0.0
            if controller.getAxisDown(controller.AXIS_L2):
                left_wheels = float(
                    controller.getAxisValue(controller.AXIS_L2))
                print left_wheels
            else:
                left_wheels = 0.0

            if reverse is True:
                left_wheels = float(-left_wheels)
                right_wheels = float(-right_wheels)

        except ValueError:
            left_wheels = "0"
            right_wheels = "0"

	left_wheels = 50
	right_wheels = 50
        #if right_wheels != prev_right or left_wheels != prev_left:
        out_wheels_pipe.send((float(left_wheels), float(right_wheels)))

        prev_left = float(left_wheels)
        prev_right = float(right_wheels)

        if controller.getButtonDown(controller.BTN_CIRCLE):
            square_pressed = True
            out_run_prog_pipe.send(False)

        sleep(.1)

