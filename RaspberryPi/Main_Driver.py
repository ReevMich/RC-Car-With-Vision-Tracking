#!/usr/bin/python

# Imports
import serial
import SimpleCV
from threading import Thread
from DS4Controller.src import controller

# Global Variables
arduino = serial.Serial('/dev/ttyACM0', 9600)  # USB serial connection with baud rate of 9600
cam = SimpleCV.Camera()


# Main Method
def main():
    
    print("Serial connected on " + arduino.name)
    
    # creates a new controller object.
    ds4 = controller.newController()
    # checks if the controller is still active.
    while(ds4.active):
        if(controller.getAxisDown(controller.AXIS_R2)):
            print("R2=%d" % controller.getAxisValue(controller.AXIS_R2))

        if(controller.getAxisDown(controller.AXIS_L2)):
            print("L2=%d" % controller.getAxisValue(controller.AXIS_L2))

        if(controller.getAxisDown(controller.AXIS_LEFT_STICK_X)):
            print("LS_X=%d" % controller.getAxisValue(controller.AXIS_LEFT_STICK_X))

        if(controller.getAxisDown(controller.AXIS_LEFT_STICK_Y)):
            print("LS_Y=%d" % controller.getAxisValue(controller.AXIS_LEFT_STICK_Y))

        if(controller.getAxisDown(controller.AXIS_RIGHT_STICK_X)):
            print("RS_X=%d" % controller.getAxisValue(controller.AXIS_RIGHT_STICK_X))

        if(controller.getAxisDown(controller.AXIS_RIGHT_STICK_Y)):
            print("RS_Y=%d" % controller.getAxisValue(controller.AXIS_RIGHT_STICK_Y))

    
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
