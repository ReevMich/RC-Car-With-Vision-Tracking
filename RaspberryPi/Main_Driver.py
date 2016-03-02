#!/usr/bin/python

# Imports
import serial
import SimpleCV
from time import sleep
from threading import Thread, Event
from Queue import Queue
from DS4Controller import ControllerModule

# Global Variables

ARDUINO = serial.Serial('/dev/ttyACM0', 9600)  # USB serial connection with baud rate of 9600
CAMERA = SimpleCV.Camera()


# Main Method
def main():

    image_queue = Queue()

    controller = ControllerModule.newControllerOBJ()

    print("Serial connected on " + ARDUINO.name)

    # Thread setup and start
    camera_thread = ImageCaptureThread(CAMERA, image_queue)
    img_display_thread = ImageDisplayThread(image_queue)
    camera_thread.start()
    img_display_thread.start()

    x_pressed = False
    while controller.active and x_pressed is False:

        try:
            left_wheels = ControllerModule.getAxisValue(ControllerModule.AXIS_LEFT_STICK_Y)
            right_wheels = ControllerModule.getAxisValue(ControllerModule.AXIS_RIGHT_STICK_Y)
        except ValueError:
            left_wheels = "0"
            right_wheels = "0"

        print "Left: %d Right: %d" % (left_wheels, right_wheels)
        set_ardunio_wheel_speeds(left_wheels, right_wheels)

        if ControllerModule.getKeyDown(ControllerModule.BTN_CROSS):
            x_pressed = True

        sleep(.05)

    # Kill Threads
    camera_thread.join()
    img_display_thread.join()

    # Stop car from moving
    set_ardunio_wheel_speeds("0", "0")

    sleep(1)  # Give time for threads to close
    # Clears the image queue of all images before close
    with image_queue.mutex:
        image_queue.queue.clear()


# Takes in a wheel speed and formats it for the arduino
def format_speeds(input_speeds):

    try:
        wheel_init = int(input_speeds)
    except ValueError:
        wheel_init = 0

    wheel = str(abs(wheel_init)).zfill(3)

    if wheel_init >= 0:
        wheel = "0" + wheel
    else:
        wheel = "-" + wheel

    return wheel


# Takes in the two wheels speeds and formats them and sends them to the arduino
def set_ardunio_wheel_speeds(left, right):
    wheel_speeds = format_speeds(left) + format_speeds(right)
    ARDUINO.write(wheel_speeds)


# Class for handling streaming from webcam
class ImageCaptureThread(Thread):
    # Initial Setup for thread
    def __init__(self, camera, img_queue):
        Thread.__init__(self)
        self.cam = camera
        self.img_queue = img_queue
        self.thread_kill_request = Event()

    # Captures images and puts them in a queue
    def run(self):
        while not self.thread_kill_request.is_set():
            if self.img_queue.qsize() < 10:
                try:
                    img = CAMERA.getImage()
                    self.img_queue.put(img)
                    sleep(.05)
                except self.img_queue.Empty:
                    continue

    # Handles terminating the thread
    def join(self, timeout=None):
        self.thread_kill_request.set()
        super(ImageCaptureThread, self).join(timeout)


# Thread for handling displaying the image
class ImageDisplayThread(Thread):
    # Initial Setup for thread
    def __init__(self, img_queue):
        Thread.__init__(self)
        self.img_queue = img_queue
        self.thread_kill_request = Event()

    # Displays the image
    def run(self):
        while not self.thread_kill_request.is_set():
            try:
                img = self.img_queue.get()
                img.show()
            except self.img_queue.Empty:
                continue

    # Handles terminating the thread
    def join(self, timeout=None):
        self.thread_kill_request.set()
        super(ImageDisplayThread, self).join(timeout)


if __name__ == '__main__':
    main()
