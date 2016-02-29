#!/usr/bin/python

# Imports
import serial
import SimpleCV
from time import sleep
from threading import Thread, Event
from Queue import Queue

# Global Variables
VIRTUAL_DEV_MODE = True

if VIRTUAL_DEV_MODE:
    ARDUINO = serial.Serial('COM4', 9600)
else:
    ARDUINO = serial.Serial('/dev/ttyACM0', 9600)  # USB serial connection with baud rate of 9600

if VIRTUAL_DEV_MODE:
    CAMERA = SimpleCV.VirtualCamera("black.jpg", "image")
else:
    CAMERA = SimpleCV.Camera()


# Main Method
def main():

    image_queue = Queue()

    print("Serial connected on " + ARDUINO.name)

    # Thread setup and start
    camera_thread = ImageCaptureThread(CAMERA, image_queue)
    img_display_thread = ImageDisplayThread(image_queue)
    camera_thread.start()
    img_display_thread.start()

    command = str(raw_input("Enter Car Commands: "))
    while len(command) is not 0:

        try:
            left_wheels, right_wheels = command.split(" ")
        except ValueError:
            left_wheels = "0"
            right_wheels = "0"

        if VIRTUAL_DEV_MODE:
            formatted_wheel_speeds = "0 0"
            print "Left Wheels: %s Right Wheels: %s" % \
                  (format_wheel_speeds(left_wheels), format_wheel_speeds(right_wheels))
        else:
            formatted_wheel_speeds = format_wheel_speeds(left_wheels) + format_wheel_speeds(right_wheels)

        set_ardunio_wheel_speeds(formatted_wheel_speeds)
        command = str(raw_input("Enter Car Commands: "))

    camera_thread.join()
    img_display_thread.join()

    set_ardunio_wheel_speeds("00000000")

    sleep(1)  # Give time for threads to close
    # Clears the image queue of all images before close
    with image_queue.mutex:
        image_queue.queue.clear()


# Takes in a wheel speed and formats it for the arduino
def format_wheel_speeds(input_speeds):

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


def set_ardunio_wheel_speeds(command):
    ARDUINO.write(command)


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
