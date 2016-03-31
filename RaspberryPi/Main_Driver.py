#!/usr/bin/python

# Imports

from time import sleep
from multiprocessing import Process, Pipe
import DS4_Controller
import Arduino
import Distance_Sensor


# Main Method
def main():

    run_prog = True

    run_prog_pipe_cntrlr = Pipe()
    controller_pipe = Pipe()
    dist_pipe = Pipe()

    controller_ds4_proc = Process(target=DS4_Controller.main,
                                  args=(controller_pipe, run_prog_pipe_cntrlr))

    arduino_proc = Process(target=Arduino.main, args=(controller_pipe,
                                                      dist_pipe))

    distance_proc = Process(target=Distance_Sensor.main, args=(dist_pipe,))

    controller_ds4_proc.start()
    arduino_proc.start()
    distance_proc.start()

    while run_prog:
        try:
            run_prog = run_prog_pipe_cntrlr.get()
            print "Program Should terminate:" + str(run_prog)
        except run_prog_pipe_cntrlr.empty():
            pass

        sleep(1)

    controller_ds4_proc.terminate()
    distance_proc.terminate()
    sleep(1)
    arduino_proc.terminate()

if __name__ == '__main__':
    main()
