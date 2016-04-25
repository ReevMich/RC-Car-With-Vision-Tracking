#!/usr/bin/python

import wiringpi
from time import sleep

# GPIO pins for the wheels
LEFT_FORWARD = 17
LEFT_BACKWARD = 4
RIGHT_FORWARD = 27
RIGHT_BACKWARD = 22


def main(arduino_wheel_speeds_pipe, dist_sensor_pipe, ball_tracker_pipe):

    program_running = True
    distance_sensor_triggered = False

    _, in_wheel_speed_pipe = arduino_wheel_speeds_pipe
    _, in_dist_sensor_pipe = dist_sensor_pipe
    _, in_ball_tracker_pipe = ball_tracker_pipe

    setup_gpio()

    # default wheel speeds
    left_wheel, right_wheel, prev_left, prev_right = (0, 0, 0, 0)

    while program_running:

        # if the distance sensor was triggered
        if in_dist_sensor_pipe.poll():
            distance_sensor_triggered = in_dist_sensor_pipe.recv()
            print distance_sensor_triggered

        # if the controller is sending data
        if in_wheel_speed_pipe.poll():
            prev_left, prev_right = left_wheel, right_wheel
            left_wheel, right_wheel = in_wheel_speed_pipe.recv()

        # ball tracker wheel speeds
        if in_ball_tracker_pipe.poll():
            prev_left, prev_right = left_wheel, right_wheel
            left_wheel, right_wheel = in_ball_tracker_pipe.recv()

        # if we aren't trying to hit something
        if distance_sensor_triggered is False:
            #if prev_left != left_wheel or prev_right != right_wheel:
                #print "Arduino Left: %.2f Right: %.2f" % \
                #      (left_wheel, right_wheel)
            set_wheel_speeds(left_wheel, LEFT_FORWARD, LEFT_BACKWARD)
            set_wheel_speeds(right_wheel, RIGHT_FORWARD, RIGHT_BACKWARD)
        else:  # if we are trying to hit something we should reverse
            #print "Triggered Arduino Left: %.2f Right: %.2f" % (-0.3, -0.3)
            set_wheel_speeds(-30, LEFT_FORWARD, LEFT_BACKWARD)
            set_wheel_speeds(-30, RIGHT_FORWARD, RIGHT_BACKWARD)

        sleep(.001)


# Configure the gpio pins
def setup_gpio():
    wiringpi.wiringPiSetupGpio()

    wiringpi.pinMode(LEFT_FORWARD, 1)
    wiringpi.pinMode(LEFT_BACKWARD, 1)
    wiringpi.pinMode(RIGHT_FORWARD, 1)
    wiringpi.pinMode(RIGHT_BACKWARD, 1)

    wiringpi.softPwmCreate(LEFT_FORWARD, 0, 100)
    wiringpi.softPwmCreate(LEFT_BACKWARD, 0, 100)
    wiringpi.softPwmCreate(RIGHT_FORWARD, 0, 100)
    wiringpi.softPwmCreate(RIGHT_BACKWARD, 0, 100)


# Set the wheels speeds
# integer speed >= -90 <= 90
# integer forward - GPIO pin number for forward
# integer backward - GPIO pin number for backwards
def set_wheel_speeds(speed, forward, backward):
    abs_speed = int(abs(speed))

    if abs_speed < 10 and abs_speed != 0:
        abs_speed = 10
    elif abs_speed > 90:
        abs_speed = 90

    if speed >= 0:
        wiringpi.softPwmWrite(forward, abs_speed)
        wiringpi.softPwmWrite(backward, 0)
    else:
        print "BackWard %d" % abs_speed
        wiringpi.softPwmWrite(forward, 0)
        wiringpi.softPwmWrite(backward, abs_speed)

