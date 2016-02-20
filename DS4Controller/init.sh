#!/bin/bash
echo -e 'power on\nconnect AC:FD:93:89:6A:01 \n quit' | bluetoothctl
echo -e 'info AC:FD:93:89:6A:01 \n quit' | bluetoothctl | grep Connected | sed 's/Connected:\| \| ;//g' | tr -d ' ' > log.txt

connected=`grep "no" log.txt `

if [ "$connected"="no" ]
then
    echo "NO"
else
    echo "YES"
fi
