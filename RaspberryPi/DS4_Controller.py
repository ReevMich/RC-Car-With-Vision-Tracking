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

    reverse_countdown = 0

    while ds4_controller.active and square_pressed is False:

        reverse_countdown -= 1
        if controller.getButtonDown(controller.BTN_SQUARE):
            print str(reverse)
            reverse = not reverse
            reverse_countdown = 5

        try:
            if controller.getAxisDown(controller.AXIS_R2):
                right_wheels = controller.getAxisValue(controller.AXIS_R2)
            else:
                right_wheels = 0
            if controller.getAxisDown(controller.AXIS_L2):
                left_wheels = controller.getAxisValue(controller.AXIS_L2)
            else:
                left_wheels = 0

            if reverse is True:
                left_wheels = -left_wheels
                right_wheels = -right_wheels

        except ValueError:
            left_wheels = 0
            right_wheels = 0

        if right_wheels != prev_right or left_wheels != prev_left:
            out_wheels_pipe.send((left_wheels * 100, right_wheels * 100))

        prev_left = left_wheels
        prev_right = right_wheels

        if controller.getButtonDown(controller.BTN_CIRCLE):
            square_pressed = True
            out_run_prog_pipe.send(False)

        sleep(.1)
