#!/bin/bash
## makes compiling the controller module much easoer and faster
cc -pthread -c *.c

status1=$?

if [ "$status1" -eq 0 ]; then
    cc -pthread -o controller *.o
fi

status2=$?
if [ "$status1" -eq 0 ] && [ "$status2" -eq 0 ]; then
    ./controller
fi
