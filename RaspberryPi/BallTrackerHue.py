#!/usr/bin/env python

import SimpleCV
from time import sleep

SPEED_MULTIPLIER = 3  # MAX 10
test = False
POWER = 8 * SPEED_MULTIPLIER + 10


def main(out_wheels_pipe):

    #display = SimpleCV.Display()
    cam = SimpleCV.Camera()

    img = cam.getImage()

    center_width = img.width/2.0
    center_height = img.height/2.0
    percentage_middle = center_width * .05

    print "Center Width: %.2f" % center_width
    print "Center Height: %.2f" % center_height
    print "Percentage Middle: %.2f" % percentage_middle
    
    if not test:
        out_wheels, _ = out_wheels_pipe

    while True:
        #if display.mouseRight:
        #    normal_display = not normal_display
        #    print "Display Mode:", "Normal" if normal_display else "Segmented"
        print "img loop"
        img = cam.getImage()
        dist = img.colorDistance(SimpleCV.Color.ORANGE).dilate(2)
        segmented = dist.stretch(200, 255)
        blobs = segmented.findBlobs()
        if blobs:
            circles = blobs.filter([b.isCircle(0.2) for b in blobs])
            if circles:
                x = circles[-1].x
                y = circles[-1].y
                #img.drawCircle((x, y), circles[-1].radius(), SimpleCV.Color.BLUE, 3)

                if x < (center_width - percentage_middle):
                    x_percentage = float(x) / (center_width - percentage_middle)
                    print "LEFT: NON ABS: x_percentage %.2f" % x_percentage
                    x_percentage = -1.0*(x_percentage - 1)
                    print "LEFT: ABS: x_percentage %.2f" % x_percentage
                    left_wheel = x_percentage * POWER
                    right_wheel = -x_percentage * POWER
                elif x > (center_width + percentage_middle):
                    x_percentage = float(x) / (center_width + percentage_middle)
                    print "RIGHT: NON ABS: x_percentage %.2f" % x_percentage
                    x_percentage = -1.0*(x_percentage - 2)
                    print "RIGHT: ABS: x_percentage %.2f" % x_percentage
                    left_wheel = -x_percentage * POWER
                    right_wheel = x_percentage * POWER
                else:
                    left_wheel = POWER
                    right_wheel = POWER
                
                #print "Left %f Right $f" % (left_wheel, right_wheel)
                print left_wheel, right_wheel
                out_wheels.send((left_wheel, right_wheel))
            else:
                out_wheels.send((0, 0))
                print "NO BLOBS"

if __name__ == "__main__":
    main(None)

