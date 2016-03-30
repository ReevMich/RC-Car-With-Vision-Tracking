#!/usr/bin/python

# Imports

from time import sleep
from multiprocessing import Process, Queue
import DS4_Controller
import Arduino


# Main Method
def main():

    run_prog = True

    run_prog_queue_cntrlr = Queue()
    run_prog_queue_arduino = Queue()
    controller_queue = Queue()
    controller_ds4_proc = Process(target=DS4_Controller.main,
                                  args=(controller_queue, run_prog_queue_cntrlr))

    arduino_proc = Process(target=Arduino.main, args=(controller_queue,
                                                      run_prog_queue_arduino))

    controller_ds4_proc.start()
    arduino_proc.start()

    while run_prog:
        try:
            run_prog = run_prog_queue_cntrlr.get()
            run_prog_queue_arduino.put(run_prog)
            print "Program Should terminate:" + str(run_prog)
        except run_prog_queue_cntrlr.empty():
            pass

        sleep(1)

    controller_ds4_proc.join()
    arduino_proc.join()

if __name__ == '__main__':
    main()
