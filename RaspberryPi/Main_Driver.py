#!/usr/bin/python

# Imports

from time import sleep
from multiprocessing import Process, Queue
import DS4_Controller
import Arduino
import Distance_Sensor


# Main Method
def main():

    run_prog = True

    run_prog_queue_cntrlr = Queue()
    controller_queue = Queue()
    dist_queue = Queue()

    controller_ds4_proc = Process(target=DS4_Controller.main,
                                  args=(controller_queue, run_prog_queue_cntrlr))

    arduino_proc = Process(target=Arduino.main, args=(controller_queue,
                                                      dist_queue))

    distance_proc = Process(target=Distance_Sensor.main, args=(dist_queue,))

    controller_ds4_proc.start()
    arduino_proc.start()
    distance_proc.start()

    while run_prog:
        try:
            run_prog = run_prog_queue_cntrlr.get()
            print "Program Should terminate:" + str(run_prog)
        except run_prog_queue_cntrlr.empty():
            pass

        sleep(1)

    controller_queue.put(0.0, 0.0)
    controller_ds4_proc.terminate()
    distance_proc.terminate()
    sleep(1)
    arduino_proc.terminate()

if __name__ == '__main__':
    main()
