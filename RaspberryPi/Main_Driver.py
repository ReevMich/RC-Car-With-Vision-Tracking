#!/usr/bin/python

"""
EXIT CODES:
0 - Successfully terminated :)
1 - Invalid number of command line arguments
2 - -m was not passed
3 - Invalid mode argument should be 0 or 1
"""

# Imports
from time import sleep
from multiprocessing import Process, Pipe
import DS4_Controller
import Wheel_Control
import Distance_Sensor
import ball_tracking
from sys import argv, exit


# Main Method
def main():

    run_prog = True  # Keeps the program loading

    run_prog_pipe = Pipe()  # Run Program Pipe
    controller_pipe = Pipe()  # PS4 Controller Pipe
    dist_pipe = Pipe()  # Distance Sensor Pipe
    ball_tracker_pipe = Pipe()  # Ball Tracker Pipe

    controller_ds4_proc = None
    ball_tracker_proc = None

    if len(argv) is 3:
        if argv[1] == '-m':
            if argv[2] == '0':
                controller_ds4_proc = Process(target=DS4_Controller.main,
                                              args=(controller_pipe,
                                                    run_prog_pipe))

                controller_ds4_proc.start()
                print "RUNNING CONTROLLER MODE"
            elif argv[2] == '1':
                ball_tracker_proc = Process(target=ball_tracking.main,
                                            args=(ball_tracker_pipe,
                                                  run_prog_pipe))
                ball_tracker_proc.start()
                print "RUNNING BALL TRACKER MODE"
            else:
                print "0 or 1 was not specified"
                usage()
                exit(3)
        else:
            print "-m was not specified"
            usage()
            exit(2)
    else:
        print "Invalid number of arguments"
        usage()
        exit(1)

    # Configure Wheel and distance Proccess
    wheel_proc = Process(target=Wheel_Control.main, args=(controller_pipe,
                                                            dist_pipe,
                                                            ball_tracker_pipe))

    distance_proc = Process(target=Distance_Sensor.main, args=(dist_pipe,))

    # Run wheel and distance process the processes
    wheel_proc.start()
    distance_proc.start()

    # Gets the out pipe of run program
    _, in_term_prog = run_prog_pipe

    # Keep running the program until we should terminate
    while run_prog:
        run_prog = in_term_prog.recv()
        # print "Program Should terminate:" + str(not run_prog)
        sleep(1)

    # Terminate all the processes if the program should terminate
    if controller_ds4_proc is not None:
        controller_ds4_proc.terminate()

    if ball_tracker_proc is not None:
        ball_tracker_proc.terminate()

    distance_proc.terminate()
    wheel_proc.terminate()

    exit(0)


def usage():
    print "Usage:"
    print "Program needs 2 arguments"
    print "-m for specifying this will be using a mode"
    print "0 for using controller or 1 for using vision tracking"
    print "EX: sudo ./Main_Driver -m 0"


if __name__ == '__main__':
    main()
