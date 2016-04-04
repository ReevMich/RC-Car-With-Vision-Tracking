import SimpleCV

SPEED_MULTIPLIER = 10  # MAX 10


def main(out_wheels_pipe):

    #display = SimpleCV.Display()
    cam = SimpleCV.Camera()
    normal_display = True

    out_wheels, _ = out_wheels_pipe

    while True:
        print "loop2"
        #if display.mouseRight:
        #    normal_display = not normal_display
        #    print "Display Mode:", "Normal" if normal_display else "Segmented"

        img = cam.getImage().flipHorizontal()
        dist = img.colorDistance(SimpleCV.Color.BLACK).dilate(2)
        segmented = dist.stretch(200, 255)
        blobs = segmented.findBlobs()
        if blobs:
            circles = blobs.filter([b.isCircle(0.2) for b in blobs])
            if circles:
                x = circles[-1].x
                y = circles[-1].y
                img.drawCircle((x, y), circles[-1].radius(), SimpleCV.Color.BLUE, 3)

                if x <= 213:
                    if y <= 160:
                        speed = SPEED_MULTIPLIER * 5
                        print "QUAD1: %d, %d" % (speed, speed + 40)
                        out_wheels.send((speed, speed + 40))
                    elif y <= 320:
                        speed = SPEED_MULTIPLIER * 3.5
                        print "QUAD4: %d, %d" % (speed, speed + 40)
                        out_wheels.send((speed, speed + 40))
                    elif y <= 480:
                        speed = SPEED_MULTIPLIER * 2
                        print "QUAD7: %d, %d" % (speed, speed + 40)
                        out_wheels.send((speed, speed + 40))
                elif x <= 426:
                    if y <= 160:
                        speed = SPEED_MULTIPLIER * 7
                        print "QUAD2: %d, %d" % (speed, speed)
                        out_wheels.send((speed, speed))
                    elif y <= 320:
                        speed = SPEED_MULTIPLIER * 5
                        print "QUAD5: %d, %d" % (speed, speed)
                        out_wheels.send((speed, speed))
                    elif y <= 480:
                        print "QUAD8: %d, %d" % (0, 0)
                        out_wheels.send((0, 0))
                elif x <= 640:
                    if y <= 160:
                        speed = SPEED_MULTIPLIER * 5
                        print "QUAD3: %d, %d" % (speed + 40, speed)
                        out_wheels.send((speed + 40, speed))
                    elif y <= 320:
                        speed = SPEED_MULTIPLIER * 3.5
                        print "QUAD6: %d, %d" % (speed + 40, speed)
                        out_wheels.send((speed + 40, speed))
                    elif y <= 480:
                        speed = SPEED_MULTIPLIER * 2
                        print "QUAD9: %d, %d" % (speed + 40, speed)
                        out_wheels.send((speed + 40, speed))
        #if normal_display:
        #    img.show()
        #else:
        #    segmented.show()
