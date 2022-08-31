#!/bin/sh

timeout 5s python $1 2> /dev/null 1> o.out < $2
exit_status=$?
if [ $exit_status -ne 0 ]; then
    if [ $exit_status -eq 124 ]; then
        echo "Time Limit Exceeded"
    else
        echo "Runtime Error"
    fi
    exit
else
    if cmp -s o.out $3;
    then
        echo "AC" > /dev/null
    else
        echo "WA"
        exit 1
    fi
fi



