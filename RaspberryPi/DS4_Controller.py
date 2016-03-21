#!/usr/bin/python

from DS4Controller.src import controller
from time import sleep
from multiprocessing import Queue


def main(out_arduino_wheel_speed_queue):
    # init ds4 controller
    ds4_controller = controller.newController()

    # lets us know when to exit to program
    square_pressed = False

    reverse = False

    # Speed of the wheels
    left_wheels = 0
    right_wheels = 0
    prev_left = 0
    prev_right = 0

    while square_pressed is False:
        while ds4_controller.active:

            if controller.getButtonDown(controller.BTN_SQUARE):
                reverse = not reverse
                print "Reverse: " + str(reverse)

            try:
                if reverse is True:
                    left_wheels = -controller.getAxisValue(controller.AXIS_R2)
                    right_wheels = -controller.getAxisValue(controller.AXIS_L2)
                else:
                    left_wheels = controller.getAxisValue(controller.AXIS_R2)
                    right_wheels = controller.getAxisValue(controller.AXIS_L2)

            except ValueError:
                left_wheels = "0"
                right_wheels = "0"

            if prev_left != left_wheels or prev_right != right_wheels:
                out_arduino_wheel_speed_queue.put((left_wheels, right_wheels))
                print "Writing %d %d" % (left_wheels, right_wheels)

            prev_left = left_wheels
            prev_right = right_wheels

            if controller.getButtonDown(controller.BTN_PS):
                #out_program_running_queue.put(False)
                controller.shutDown(ds4_controller)

            if controller.getButtonDown(controller.BTN_SQUARE):
                square_pressed = True

            sleep(.1)


if __name__ == '__main__':
    test_arduino_queue = Queue()
    test_running_program_queue = Queue()
    main(test_arduino_queue, test_running_program_queue)
