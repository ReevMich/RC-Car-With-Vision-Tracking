# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from time import sleep

SPEED_MULTIPLIER = 5  # MAX 10
POWER = 8 * SPEED_MULTIPLIER + 10
MIN_TURN = 30
STRAIGHT_CONE_PERCENT = .45


def main(out_wheels_pipe, term_prog_pipe):
    out_wheels, _ = out_wheels_pipe
    term_prog, _ = term_prog_pipe

    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    green_lower = (29, 86, 6)
    green_upper = (64, 255, 255)

    camera = cv2.VideoCapture(0)

    center_width = 320
    percentage_mid = center_width * STRAIGHT_CONE_PERCENT

    left_wheel, right_wheel = (0, 0)

    win = False

    # keep looping
    while win is False:
        #sleep(.01)
        # grab the current frame
        (_, frame) = camera.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, green_lower, green_upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)

            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            x_coord, y_coord = center

            # Ball is on the left
            if x_coord < (center_width - percentage_mid):
                # Percentage from middle the ball is
                x_percentage = float(x_coord) / (center_width - percentage_mid)
                x_percentage = -1.0 * (x_percentage - 1) * POWER
                
                # Make sure we have a minimum speed we can turn at
                if x_percentage > MIN_TURN:
                    left_wheel = x_percentage
                    right_wheel = -x_percentage
                else:
                    left_wheel = MIN_TURN
                    right_wheel = -MIN_TURN

            # Ball is on the right
            elif x_coord > (center_width + percentage_mid):
                # Calculate the perecentage from middle the ball is
                x_percentage = float(x_coord) / (center_width + percentage_mid)
                x_percentage = -1.0 * (x_percentage - 2) * POWER

                # Make sure we have a minimum speed we can turn at
                if x_percentage > MIN_TURN:
                    left_wheel = -x_percentage
                    right_wheel = x_percentage
                else:
                    left_wheel = -MIN_TURN
                    right_wheel = MIN_TURN
            else:  # The ball is in front of us
                left_wheel = POWER
                right_wheel = POWER

            #print "Left %f Right $f" % (left_wheel, right_wheel)
            #print left_wheel, right_wheel
            out_wheels.send((left_wheel, right_wheel))
    
            if radius > 340:  # We found the ball
                win = True
                out_wheels.send((0, 0))
                term_prog.send(False)
                sleep(2)

        else:  # Keep turning if we lose track of the ball 
            out_wheels.send((left_wheel, right_wheel))
