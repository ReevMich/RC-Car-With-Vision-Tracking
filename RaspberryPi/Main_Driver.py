#!/usr/bin/python

# Imports

from time import sleep
from multiprocessing import Process, Queue
import DS4_Controller
import Arduino


# Global Variables


TRIG = 23
ECHO = 24

# Main Method
def main():

    controller_queue = Queue()
    controller_ds4_proc = Process(target=DS4_Controller.main, args=(controller_queue,))

    arduino_proc = Process(target=Arduino.main, args=(controller_queue,))

    controller_ds4_proc.start()
    arduino_proc.start()

    while True:
        pass

    sleep(1)  # Give time for threads to close

if __name__ == '__main__':
    main()
