#!/usr/bin/python

import pyfirmata
from time import sleep

ARDUINO = None

LEFT_FORWARD = None
LEFT_BACKWARD = None
RIGHT_FORWARD = None
RIGHT_BACKWARD = None

DISTANCE_SENSOR_TRIGGERED = False


def main(arduino_wheel_speeds_pipe, dist_sensor_pipe):
    global ARDUINO
    global LEFT_BACKWARD
    global LEFT_FORWARD
    global RIGHT_BACKWARD
    global RIGHT_FORWARD
    global DISTANCE_SENSOR_TRIGGERED

    program_running = True

    _, in_wheel_speed_pipe = arduino_wheel_speeds_pipe
    _, in_dist_sensor_pipe = dist_sensor_pipe

    ARDUINO = pyfirmata.Arduino('/dev/ttyACM0')

    LEFT_FORWARD = ARDUINO.get_pin('d:5:p')
    LEFT_BACKWARD = ARDUINO.get_pin('d:6:p')
    RIGHT_FORWARD = ARDUINO.get_pin('d:11:p')
    RIGHT_BACKWARD = ARDUINO.get_pin('d:10:p')

    it = pyfirmata.util.Iterator(ARDUINO)
    it.start()

    print("Serial connected on " + ARDUINO.name)

    while program_running:

        ARDUINO.analog[0].enable_reporting()
	
	if in_dist_sensor_pipe.poll():
        	DISTANCE_SENSOR_TRIGGERED = in_dist_sensor_pipe.recv()
        	print DISTANCE_SENSOR_TRIGGERED

	if in_wheel_speed_pipe.poll():
            left_wheel, right_wheel = in_wheel_speed_pipe.recv()
            print "Reading %.2f %.2f " % (left_wheel, right_wheel)
            if DISTANCE_SENSOR_TRIGGERED is False:
                set_left_wheels(left_wheel)
                set_right_wheels(right_wheel)
            else:
                set_left_wheels(-0.3)
                set_right_wheels(-0.3)

    sleep(.1)
    print("llop")

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
