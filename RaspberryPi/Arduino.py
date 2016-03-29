#!/usr/bin/python

import pyfirmata
from multiprocessing import Queue
from time import sleep

ARDUINO_IS_WRITABLE = True
ARDUINO = None

LEFT_FORWARD = None
LEFT_BACKWARD = None
RIGHT_FORWARD = None
RIGHT_BACKWARD = None


def main(arduino_wheel_speeds_queue):
    global ARDUINO
    global LEFT_BACKWARD
    global LEFT_FORWARD
    global RIGHT_BACKWARD
    global RIGHT_FORWARD
    program_running = True

    ARDUINO = pyfirmata.Arduino('/dev/ttyACM4')

    LEFT_FORWARD = ARDUINO.get_pin('d:5:p')
    LEFT_BACKWARD = ARDUINO.get_pin('d:6:p')
    RIGHT_FORWARD = ARDUINO.get_pin('d:11:p')
    RIGHT_BACKWARD = ARDUINO.get_pin('d:10:p')

    it = pyfirmata.util.Iterator(ARDUINO)
    it.start()
    
    print("Serial connected on " + ARDUINO.name)
    i = 50.0
    while program_running:

        ARDUINO.analog[0].enable_reporting()

        while ARDUINO.analog[0].read() is None:
            pass
        
        # try:
        #    program_running = program_running_queue.get()
        # except program_running_queue.empty():
        #    pass

        global ARDUINO_IS_WRITABLE

        # try:
        #    ARDUINO_IS_WRITABLE = arduino_can_move_queue.get()
        # except arduino_can_move_queue.empty():
        #    pass

        try:
#            left_wheel, right_wheel = arduino_wheel_speeds_queue.get()
            set_left_wheels(i)
            set_right_wheels(i)

            #print "Reading %d %d " % (left_wheel, right_wheel)
        except arduino_wheel_speeds_queue.empty():
            set_left_wheels(i)
            set_right_wheels(i)
            print i
            
        i -= 1.0

        if i < -50.0:
            i = 50.0
        sleep(.1)


def set_left_wheels(left):

    abs_speed = float(abs(left) / 100.0)

    if abs_speed < .1:
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
    abs_speed =float(abs(right) / 100.0)

    if abs_speed < .1:
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
