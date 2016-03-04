#!/usr/bin/python

# Imports
import serial
#import SimpleCV
from time import sleep, time
from threading import Thread, Event
from Queue import Queue
from DS4Controller.src import controller
import RPi.GPIO as GPIO


# Global Variables

ARDUINO = serial.Serial('/dev/ttyACM0', 9600)  # USB serial connection with baud rate of 9600
#CAMERA = SimpleCV.Camera()
WRITE_ARDUINO = True

TRIG = 23
ECHO = 24


# Main Method
def main():

   # GPIO.setmode(GPIO.BCM)

   # GPIO.setup(TRIG,GPIO.OUT)
   # GPIO.setup(ECHO,GPIO.IN)

   # GPIO.output(TRIG, False)
    print "Waiting For Sensor To Settle"
    #time.sleep(.5)

    #image_queue = Queue()


    print("Serial connected on " + ARDUINO.name)

    # Thread setup and start
    #camera_thread = ImageCaptureThread(CAMERA, image_queue)
    #img_display_thread = ImageDisplayThread(image_queue)
    #distance_thread = DistanceSensorThread()
    ds4_thread = DS4ControllerThread()

    #camera_thread.start()
    #img_display_thread.start()
    #distance_thread.start()
    ds4_thread.start()

    while WRITE_ARDUINO:
        me = 1;
    
    
    # Kill Threads
    #camera_thread.join()
    #img_display_thread.join()
    #distance_thread.join()
    ds4_thread.join()
    
    # Stop car from moving
    print "something died"
    set_ardunio_wheel_speeds("0", "0")

    sleep(1)  # Give time for threads to close
    # Clears the image queue of all images before close
    #with image_queue.mutex:
        #image_queue.queue.clear()


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


#Thread for handling the Dual Shock 4 Controller
class DS4ControllerThread(Thread):
    # Init
    def __init__(self):
        Thread.__init__(self)
        self.thread_kill_request = Event()

    def run(self):
        global WRITE_ARDUINO
        ds4_controller = controller.newController()
        ps_pressed = False
        left_wheels = 0
        right_wheels = 0
        prev_left_value = 0
        prev_right_value = 0
        valuesChanged = False
        while not self.thread_kill_request.is_set() and ds4_controller.active and ps_pressed is False:
            if WRITE_ARDUINO :
                try:
                    left_value = controller.getAxisValue(controller.AXIS_R2)
                    right_value = controller.getAxisValue(controller.AXIS_L2)

                    valuesChanged = False
                    
                    if(prev_left_value != left_value):
                        left_wheels = left_value
                        valuesChanged = True
                    if(prev_right_value != right_value):
                        right_wheels = right_value
                        valuesChanged = True
                except ValueError:
                    left_wheels = "0"
                    right_wheels = "0"

                print "Left: %d Right: %d" % (left_wheels, right_wheels)
                if(valuesChanged == True):
                    prev_left_value = left_wheels
                    prev_right_value = right_wheels
                    set_ardunio_wheel_speeds(left_wheels, right_wheels)

                if controller.getButtonDown(controller.BTN_PS):
                    controller.shutDown(ds4_controller)
                    ps_pressed = True
                sleep(.05)

    # Handles terminating the thread
    def join(self, timeout=None):
        self.thread_kill_request.set()
        super(DS4ControllerThread, self).join(timeout)

            


# Thread for handling distance Sensor
class DistanceSensorThread(Thread):
    # Initial Setup for thread
    def __init__(self):
        Thread.__init__(self)
        self.thread_kill_request = Event()

    # Runs the sensor
    def run(self):
        global WRITE_ARDUINO
        while not self.thread_kill_request.is_set():
            sleep(.25)

            GPIO.output(TRIG, True)
            sleep(0.00001)
            GPIO.output(TRIG, False)

            pulse_start, pulse_end = (0, 0)

            while GPIO.input(ECHO) == 0:
                pulse_start = time()

            while GPIO.input(ECHO) == 1:
                pulse_end = time()

            pulse_duration = pulse_end - pulse_start

            distance = pulse_duration * 17150

            distance = round(distance, 2)
            print "Distance: %f cm" % distance

            if distance < 20.0:
                WRITE_ARDUINO = False
            else:
                WRITE_ARDUINO = True

    # Handles terminating the thread
    def join(self, timeout=None):
        self.thread_kill_request.set()
        super(DistanceSensorThread, self).join(timeout)


if __name__ == '__main__':
    main()
