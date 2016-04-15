import SimpleCV
from time import sleep

SPEED_MULTIPLIER = 5  # MAX 10


def main(out_wheels_pipe):

	#display = SimpleCV.Display()
    cam = SimpleCV.Camera()
    normal_display = True

    out_wheels, _ = out_wheels_pipe

    while True:
        #if display.mouseRight:
        #    normal_display = not normal_display
        #    print "Display Mode:", "Normal" if normal_display else "Segmented"

        img = cam.getImage()
        dist = img.colorDistance(SimpleCV.Color.BLACK).dilate(2)
        segmented = dist.stretch(200, 255)
        blobs = segmented.findBlobs()
        if blobs:
            circles = blobs.filter([b.isCircle(0.2) for b in blobs])
            if circles:
                x = circles[-1].x
                y = circles[-1].y
                img.drawCircle((x, y), circles[-1].radius(), SimpleCV.Color.BLUE, 3)

                speed, turn_speed = (0, 0)

                if x <= 213:
                    if y <= 160:
                        speed = SPEED_MULTIPLIER * 5
                        print "QUAD1: ",
                    elif y <= 320:
                        speed = SPEED_MULTIPLIER * 3.5
                        print "QUAD4: ",
                    elif y <= 480:
                        speed = SPEED_MULTIPLIER * 2
                        print "QUAD7: ",

                    turn_speed = speed + 4 * SPEED_MULTIPLIER
                    out_wheels.send((speed, turn_speed))
                    print "%d %d" % (speed, turn_speed)

                elif x <= 426:
                    if y <= 160:
                        speed = SPEED_MULTIPLIER * 7
                        print "QUAD2: %d, %d" % (speed, speed)
                    elif y <= 320:
                        speed = SPEED_MULTIPLIER * 5
                        print "QUAD5: %d, %d" % (speed, speed)
                    elif y <= 480:
                        speed = 0
                        print "QUAD8: %d, %d" % (0, 0)

                    out_wheels.send((speed, speed))
                elif x <= 640:
                    if y <= 160:
                        speed = SPEED_MULTIPLIER * 5
                        print "QUAD3: ",
                    elif y <= 320:
                        speed = SPEED_MULTIPLIER * 3.5
                        print "QUAD6: ",
                    elif y <= 480:
                        speed = SPEED_MULTIPLIER * 2
                        print "QUAD9: ",

                    turn_speed = speed + 4 * SPEED_MULTIPLIER
                    out_wheels.send((turn_speed, speed))
                    print "%d %d" % (turn_speed, speed)
        sleep(.05)
        #if normal_display:
        #    img.show()
        #else:
        #    segmented.show()
