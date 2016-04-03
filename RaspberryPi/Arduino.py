#!/usr/bin/python

import wiringpi
from time import sleep

LEFT_FORWARD = 17
LEFT_BACKWARD = 4
RIGHT_FORWARD = 27
RIGHT_BACKWARD = 22

DISTANCE_SENSOR_TRIGGERED = False


def main(arduino_wheel_speeds_pipe, dist_sensor_pipe):

    global DISTANCE_SENSOR_TRIGGERED

    program_running = True

    _, in_wheel_speed_pipe = arduino_wheel_speeds_pipe
    _, in_dist_sensor_pipe = dist_sensor_pipe

    wiringpi.wiringPiSetupGpio()

    wiringpi.pinMode(LEFT_FORWARD, 1)
    wiringpi.pinMode(LEFT_BACKWARD, 1)
    wiringpi.pinMode(RIGHT_FORWARD, 1)
    wiringpi.pinMode(RIGHT_BACKWARD, 1)

    wiringpi.softPwmCreate(LEFT_FORWARD, 0, 100)
    wiringpi.softPwmCreate(LEFT_BACKWARD, 0, 100)
    wiringpi.softPwmCreate(RIGHT_FORWARD, 0, 100)
    wiringpi.softPwmCreate(RIGHT_BACKWARD, 0, 100)

    left_wheel, right_wheel = (0, 0)

    while program_running:

        if in_dist_sensor_pipe.poll():
            DISTANCE_SENSOR_TRIGGERED = in_dist_sensor_pipe.recv()
            print DISTANCE_SENSOR_TRIGGERED

        if in_wheel_speed_pipe.poll():
            prev_left, prev_right = left_wheel, right_wheel
            left_wheel, right_wheel = in_wheel_speed_pipe.recv()
        #   if prev_left != left_wheel or prev_right != right_wheel:
            if DISTANCE_SENSOR_TRIGGERED is False:
                print "Arduino Left: %.2f Right: %.2f" % \
                      (left_wheel, right_wheel)
                set_left_wheels(left_wheel)
                set_right_wheels(right_wheel)
            else:
                print "Arduino Left: %.2f Right: %.2f" % (-0.3, -0.3)
                set_left_wheels(-30)
                set_right_wheels(-30)

        sleep(.05)


def set_left_wheels(left):
    abs_speed = int(left)
    print "set left"
    if abs_speed < 10 and abs_speed != 0:
        abs_speed = 10
    elif abs_speed > 90:
        abs_speed = 90

    if left >= 0:
        wiringpi.softPwmWrite(LEFT_FORWARD, abs_speed)
        wiringpi.softPwmWrite(LEFT_BACKWARD, 0)
    else:
        wiringpi.softPwmWrite(LEFT_FORWARD, 0)
        wiringpi.softPwmWrite(LEFT_BACKWARD, abs_speed)


def set_right_wheels(right):
    abs_speed = int(right)

    if abs_speed < 10 and abs_speed != 0:
        abs_speed = 10
    elif abs_speed > 90:
        abs_speed = 90

    if right >= 0:
        wiringpi.softPwmWrite(RIGHT_FORWARD, abs_speed)
        wiringpi.softPwmWrite(RIGHT_BACKWARD, 0)
    else:
        wiringpi.softPwmWrite(RIGHT_FORWARD, 0)
        wiringpi.softPwmWrite(RIGHT_BACKWARD, abs_speed)
