#!/usr/bin/python

# Imports
import serial
import SimpleCV
from threading import Thread

# Global Variables
arduino = serial.Serial('/dev/ttyACM0', 9600)  # USB serial connection with baud rate of 9600
cam = SimpleCV.Camera()


# Main Method
def main():

    print("Serial connected on " + arduino.name)
    camera_thread = ImageThread(cam)
    camera_thread.start()
    while True:
        command = raw_input("Enter Car Commands: ")
        set_ardunio_wheel_speeds(command)


def set_ardunio_wheel_speeds(command):
    arduino.write(command)


# Class for handling streaming from webcam
class ImageThread(Thread):
    def __init__(self, camera):
        Thread.__init__(self)
        self.cam = camera

    def run(self):
        while True:
            img = cam.getImage()
            img.show()


if __name__ == '__main__':
    main()
