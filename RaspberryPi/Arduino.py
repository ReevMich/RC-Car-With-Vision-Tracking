#!/usr/bin/python

import pyfirmata
from multiprocessing import Queue
from time import sleep

ARDUINO_IS_WRITABLE = False
ARDUINO = None

LEFT_FORWARD = None
LEFT_BACKWARD = None
RIGHT_FORWARD = None
RIGHT_BACKWARD = None


def main(arduino_wheel_speeds_queue, run_prog):
    global ARDUINO
    global LEFT_BACKWARD
    global LEFT_FORWARD
    global RIGHT_BACKWARD
    global RIGHT_FORWARD
    global ARDUINO_IS_WRITABLE
    program_running = True

    ARDUINO = pyfirmata.Arduino('/dev/ttyACM0')

    LEFT_FORWARD = ARDUINO.get_pin('d:5:p')
    LEFT_BACKWARD = ARDUINO.get_pin('d:6:p')
    RIGHT_FORWARD = ARDUINO.get_pin('d:11:p')
    RIGHT_BACKWARD = ARDUINO.get_pin('d:10:p')

    it = pyfirmata.util.Iterator(ARDUINO)
    it.start()
    
    print("Serial connected on " + ARDUINO.name)
    ARDUINO_IS_WRITABLE = True

    while program_running:

        ARDUINO.analog[0].enable_reporting()
        
        try:
            left_wheel, right_wheel = arduino_wheel_speeds_queue.get()
            print "Reading %.2f %.2f " % (left_wheel, right_wheel)
            set_left_wheels(left_wheel)
            set_right_wheels(right_wheel)
        except arduino_wheel_speeds_queue.empty():
            pass

        
        sleep(.1)


def set_left_wheels(left):
    
    abs_speed = left

    if abs_speed < .1 and abs_speed != 0:
        abs_speed = .1
    elif abs_speed > .9:
        abs_speed = .9

    if left >= 0:
        LEFT_FORWARD.write(abs_speed)
        LEFT_BACKWARD.write(0.0)
        print "Forward %f" % abs_speed
    else:
        print "Backward %f" % abs_speed
        LEFT_FORWARD.write(0.0)
        LEFT_BACKWARD.write(abs_speed)


def set_right_wheels(right):
    abs_speed = right

    if abs_speed < .1 and abs_speed != 0:
        abs_speed = .1
    elif abs_speed > .9:
        abs_speed = .9

    if right >= 0:
        RIGHT_FORWARD.write(abs_speed)
        RIGHT_BACKWARD.write(0.0)
    else:
        RIGHT_FORWARD.write(0.0)
        RIGHT_BACKWARD.write(abs_speed)

if __name__ == '__main__':
    test_arduino_can_move_queue = Queue()
    test_arduino_wheels_speeds_queue = Queue()
    test_program_running_in_queue = Queue()

    # main(test_arduino_can_move_queue, test_arduino_wheels_speeds_queue, test_program_running_in_queue)
