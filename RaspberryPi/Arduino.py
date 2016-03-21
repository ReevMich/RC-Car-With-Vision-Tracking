#!/usr/bin/python

import serial
from multiprocessing import Queue
from time import sleep

ARDUINO_IS_WRITABLE = True


def main(ardrino_wheel_speeds_queue):

    program_running = True

    while program_running:
        arduino = serial.Serial('/dev/ttyACM0', 9600)
        print("Serial connected on " + arduino.name)
        while arduino.is_open:

            #try:
            #    program_running = program_running_queue.get()
            #except program_running_queue.empty():
            #    pass

            global ARDUINO_IS_WRITABLE

            #try:
            #    ARDUINO_IS_WRITABLE = arduino_can_move_queue.get()
            #except arduino_can_move_queue.empty():
            #    pass

            try:
                left_wheel, right_wheel = ardrino_wheel_speeds_queue.get()
                set_ardunio_wheel_speeds(left_wheel, right_wheel)
                print "Reading %d %d " % (left_wheel, right_wheel)
            except ardrino_wheel_speeds_queue.empty():
                pass

            sleep(.095)


# Takes in a wheel speed and formats it for the arduino
def format_speeds(input_speeds):
    try:
        wheel_init = int(input_speeds)
    except ValueError:
        wheel_init = 0

    wheel = str(abs(wheel_init)).zfill(3)

    if wheel_init >= 0:
        wheel = "0" + wheel
    else:
        wheel = "-" + wheel

    return wheel


# Takes in the two wheels speeds and formats them and sends them to the arduino
def set_ardunio_wheel_speeds(left, right):
    if ARDUINO_IS_WRITABLE:
        wheel_speeds = format_speeds(left) + format_speeds(right)
        arduino.write(wheel_speeds)
    else:
        arduino.write("00000000")


if __name__ == '__main__':
    test_arduino_can_move_queue = Queue()
    test_arduino_wheels_speeds_queue = Queue()
    test_program_running_in_queue = Queue()
    #main(test_arduino_can_move_queue, test_arduino_wheels_speeds_queue, test_program_running_in_queue)
