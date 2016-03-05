#!/usr/bin/python

from multiprocessing import Queue
import RPi.GPIO as GPIO
from time import sleep, time

TRIG = 23
ECHO = 24


def main(in_program_running_queue, out_stop_moving_queue):

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    print "Waiting For Sensor To Settle"
    sleep(.5)

    program_running = True

    while program_running:

        try:
            program_running = in_program_running_queue.get()
        except in_program_running_queue.empty():
            pass

        sleep(.5)

        GPIO.output(TRIG, True)
        sleep(0.00001)
        GPIO.output(TRIG, False)

        pulse_start, pulse_end = (0, 0)

        while GPIO.input(ECHO) == 0:
            pulse_start = time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        distance = round(distance, 2)
        print "Distance: %f cm" % distance

        if distance < 20.0:
            out_stop_moving_queue.put(False)
        else:
            out_stop_moving_queue.put(True)

if __name__ == '__main__':
    test_out_queue = Queue()
    test_in_queue = Queue()
    main(test_in_queue, test_out_queue)
