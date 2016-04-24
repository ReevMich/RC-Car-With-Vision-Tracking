#!/usr/bin/python

# Imports

from time import sleep
from multiprocessing import Process, Pipe
import DS4_Controller
import Wheel_Control
import Distance_Sensor
import BallTracker


# Main Method
def main():

    run_prog = True

    run_prog_pipe_cntrlr = Pipe()
    controller_pipe = Pipe()
    dist_pipe = Pipe()
    ball_tracker_pipe = Pipe()

    controller_ds4_proc = Process(target=DS4_Controller.main,
                                  args=(controller_pipe, run_prog_pipe_cntrlr))

    arduino_proc = Process(target=Wheel_Control.main, args=(controller_pipe,
                                                            dist_pipe,
                                                            ball_tracker_pipe))

    distance_proc = Process(target=Distance_Sensor.main, args=(dist_pipe,))
    ball_tracker_proc = Process(target=BallTracker.main,
                                args=(ball_tracker_pipe,))

    arduino_proc.start()
    controller_ds4_proc.start()
    distance_proc.start()
    ball_tracker_proc.start()

    _, in_term_prog = run_prog_pipe_cntrlr

    while run_prog:
        run_prog = in_term_prog.recv()
        print "Program Should terminate:" + str(not run_prog)

        sleep(1)

    controller_ds4_proc.terminate()
    distance_proc.terminate()
    arduino_proc.terminate()
    ball_tracker_proc.terminate()

if __name__ == '__main__':
    main()
