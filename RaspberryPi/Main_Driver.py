#!/usr/bin/python

# Imports

import SimpleCV
from time import sleep
from multiprocessing import Process, Queue
from DS4Controller.src import controller
import RPi.GPIO as GPIO


# Global Variables

ARDUINO = serial.Serial('/dev/ttyACM0', 9600)  # USB serial connection with baud rate of 9600
#CAMERA = SimpleCV.Camera()
WRITE_ARDUINO = True
PROGRAM_RUNNING = True

TRIG = 23
ECHO = 24

# Main Method
def main():
    image_queue = Queue()

    #print("Serial connected on " + ARDUINO.name)

    # Process setup and start
   # camera_capture_proc = Process(target=image_get_camera_image, args=(image_queue, CAMERA))
    #camera_disp_proc = Process(target=image_processor_and_display, args=(image_queue,))
    #dist_sensor_prc = Process(target=distance_sensor)
    controller_ds4_proc = Process(target=ds4_controller_process)
    
    #dist_sensor_prc.start()
    controller_ds4_proc.start()

    image_get_camera_image(image_queue, CAMERA)

    #ds4_controller_process()

    # Kills all threads and processes if not terminated yet
    arduino_process.join()
    ds4_controller_process.join()
    dist_sensor_process.join()
    image_thread.join()

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
    if WRITE_ARDUINO:
        wheel_speeds = format_speeds(left) + format_speeds(right)
        ARDUINO.write(wheel_speeds)


def ds4_controller_process():
    global WRITE_ARDUINO

    # init ds4 controller
    ds4_controller = controller.newController()

    # lets us know when to exit to program
    ps_pressed = False

    # toggle for reverse
    reverse = False

    # Speed of the wheels
    left_wheels = 0
    right_wheels = 0

    # Keeps track of the previous values so that way we don't have to always send messages to the arduino.
    prev_left_value = 0
    prev_right_value = 0

    # lets us know is any of the wheels values has changed.
    values_changed = False
    while ds4_controller.active and ps_pressed is False:
        if WRITE_ARDUINO:
            if controller.getButtonDown(controller.BTN_SQUARE):
                reverse = True
                #print "Reverse: On"
            else:
                reverse = False

            try:
                if reverse is True:
                    left_value = -controller.getAxisValue(controller.AXIS_R2)
                    right_value = -controller.getAxisValue(controller.AXIS_L2)
                else:
                    left_value = controller.getAxisValue(controller.AXIS_R2)
                    right_value = controller.getAxisValue(controller.AXIS_L2)

def distance_sensor():
    global WRITE_ARDUINO

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    print "Waiting For Sensor To Settle"
    sleep(.5)

    while PROGRAM_RUNNING:
        sleep(.5)

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
        #print "Distance: %f cm" % distance


if __name__ == '__main__':
    main()
