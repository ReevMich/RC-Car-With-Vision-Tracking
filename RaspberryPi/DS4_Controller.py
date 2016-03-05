#!/usr/bin/python

from DS4Controller.src import controller
from time import sleep
from multiprocessing import Queue


def main(out_arduino_wheel_speed_queue, out_program_running_queue):
    # init ds4 controller
    ds4_controller = controller.newController()

    # lets us know when to exit to program
    ps_pressed = False

    # Speed of the wheels
    left_wheels = 0
    right_wheels = 0

    # Keeps track of the previous values so that way we don't have to always send messages to the arduino.
    prev_left_value = 0
    prev_right_value = 0

    # lets us know is any of the wheels values has changed.
    values_changed = False

    while ds4_controller.active and ps_pressed is False:

        if controller.getButtonDown(controller.BTN_SQUARE):
            reverse = True
            print "Reverse: On"
        else:
            reverse = False

        try:
            if reverse is True:
                left_value = -controller.getAxisValue(controller.AXIS_R2)
                right_value = -controller.getAxisValue(controller.AXIS_L2)
            else:
                left_value = controller.getAxisValue(controller.AXIS_R2)
                right_value = controller.getAxisValue(controller.AXIS_L2)

            values_changed = False

            if prev_left_value != left_value:
                left_wheels = left_value
                values_changed = True

            if prev_right_value != right_value:
                right_wheels = right_value
                values_changed = True

        except ValueError:
            left_wheels = "0"
            right_wheels = "0"

        print "Left: %d Right: %d" % (left_wheels, right_wheels)
        if values_changed is True:
            prev_left_value = left_wheels
            prev_right_value = right_wheels
            out_arduino_wheel_speed_queue.put((left_wheels, right_wheels))

        if controller.getButtonDown(controller.BTN_PS):
            out_program_running_queue.put(False)
            controller.shutDown(ds4_controller)
            ps_pressed = True

        sleep(.1)


if __name__ == '__main__':
    test_arduino_queue = Queue()
    test_running_program_queue = Queue()
    main(test_arduino_queue, test_running_program_queue)
