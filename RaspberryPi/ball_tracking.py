# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

SPEED_MULTIPLIER = 6  # MAX 10
POWER = 8 * SPEED_MULTIPLIER + 10


def main(out_wheels_pipe):
    out_wheels, _ = out_wheels_pipe

    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    green_lower = (29, 86, 6)
    green_upper = (64, 255, 255)

    camera = cv2.VideoCapture(0)

    center_width = 320
    percentage_middle = center_width * .05

    # keep looping
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()

        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
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

            print center
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

            # show the frame to our screen
            cv2.imshow("Frame", frame)

            x_coord, y_coord = center

            if x_coord < (center_width - percentage_middle):
                x_percentage = float(x_coord) / (center_width - percentage_middle)
                print "LEFT: NON ABS: x_percentage %.2f" % x_percentage
                x_percentage = -1.0 * (x_percentage - 1) * POWER
                print "LEFT: ABS: x_percentage %.2f" % x_percentage
                if x_percentage > 30:
                    left_wheel = x_percentage
                    right_wheel = -x_percentage
                else:
                    left_wheel = 30
                    right_wheel = -30
            elif x_coord > (center_width + percentage_middle):
                x_percentage = float(x_coord) / (center_width + percentage_middle)
                print "RIGHT: NON ABS: x_percentage %.2f" % x_percentage
                x_percentage = -1.0 * (x_percentage - 2) * POWER
                print "RIGHT: ABS: x_percentage %.2f" % x_percentage
                if x_percentage > 30:
                    left_wheel = -x_percentage
                    right_wheel = x_percentage
                else:
                    left_wheel = -30
                    right_wheel = 30
            else:
                left_wheel = POWER
                right_wheel = POWER

            # print "Left %f Right $f" % (left_wheel, right_wheel)
            print left_wheel, right_wheel
            out_wheels.send((left_wheel, right_wheel))
        else:
            out_wheels.send((0, 0))
            print "NO BLOBS"


            # only proceed if the radius meets a minimum size


# cleanup the camera and close any open windows
# camera.release()
# cv2.destroyAllWindows()
