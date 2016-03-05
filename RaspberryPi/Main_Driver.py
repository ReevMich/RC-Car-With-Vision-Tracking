#!/usr/bin/python

# Imports

import SimpleCV
from time import sleep
from multiprocessing import Process, Queue
from threading import Thread, Event
import Arduino
import DS4_Controller
import Distance_Sensor


# Main Method
def main():

    # Setup Queues when Processes should terminate
    run_ardrino_process_queue = Queue()
    run_distance_sensor_queue = Queue()
    controller_program_running_queue = Queue()

    # Setup wheel control queues
    arduino_wheel_speed_queue = Queue()
    arduino_moving_queue = Queue()

    # keeps the program running
    run_program = True

    # Setup Processes
    arduino_process = Process(target=Arduino.main, args=(arduino_moving_queue,
                                                         arduino_wheel_speed_queue,
                                                         run_ardrino_process_queue))
    ds4_controller_process = Process(target=DS4_Controller.main, args=(arduino_wheel_speed_queue,
                                                                       controller_program_running_queue))
    dist_sensor_process = Process(target=Distance_Sensor.main, args=(run_distance_sensor_queue,
                                                                     arduino_moving_queue))
    # Setup Threads
    image_thread = ImageProcessing()

    # Start Processes and Threads
    arduino_process.start()
    ds4_controller_process.start()
    dist_sensor_process.start()
    image_thread.start()

    # Keeps everything running
    while run_program:
        try:
            run_program = controller_program_running_queue.get()
            run_ardrino_process_queue.put(run_program)
            run_distance_sensor_queue.put(run_program)
        except controller_program_running_queue.empty():
            pass

        sleep(1)

    # Kills all threads and processes if not terminated yet
    arduino_process.join()
    ds4_controller_process.join()
    dist_sensor_process.join()
    image_thread.join()

    sleep(1)  # Give time for threads to close


# Class for handling image processing
class ImageProcessing(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.cam = SimpleCV.Camera()
        self.thread_kill_request = Event()

    # Captures images and puts them in a queue
    def run(self):
        while not self.thread_kill_request.is_set():
            img = self.cam.getImage()
            img.show()
            sleep(.1)

    # Handles terminating the thread
    def join(self, timeout=None):
        self.thread_kill_request.set()
        super(ImageProcessing, self).join(timeout)


if __name__ == '__main__':
    main()
