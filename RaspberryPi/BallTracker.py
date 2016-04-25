import SimpleCV
from time import sleep

SPEED_MULTIPLIER = 5  # MAX 10
test = False

def main(out_wheels_pipe):

    cam = SimpleCV.Camera()

    if not test:
        out_wheels, _ = out_wheels_pipe

    while True:
        print "Camera loop"
        img = cam.getImage()
        dist = img.colorDistance(SimpleCV.Color.ORANGE).dilate(2)
        segmented = dist.stretch(200, 255)
        blobs = segmented.findBlobs()
        if blobs:
            circles = blobs.filter([b.isCircle(0.2) for b in blobs])
            if circles:
                x = circles[-1].x
                y = circles[-1].y
                img.drawCircle((x, y), circles[-1].radius(), SimpleCV.Color.BLUE, 3)

                if not test:
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
                    
                    if not test:
                        out_wheels.send((turn_speed, -speed))
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
                        print "QUAD8: %d, %d" % (speed, speed)
                    
                    if not test:
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
                   
                    if not test:
                        out_wheels.send((-speed, turn_speed))
                    print "%d %d" % (turn_speed, speed)

        if test:
            img.show()
        sleep(.01)

if __name__ == "__main__":
    main(None)
