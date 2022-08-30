#!/bin/sh

g++ $1 2> /dev/null
exit_status=$?
if [ $exit_status -ne 0 ]; then
    echo "Compilation Error"
    exit 1
fi
timeout 5s ./a.out 1> o.out 2> /dev/null < $2
exit_status=$?
if [ $exit_status != 0 ]; then
    if [ $exit_status -eq 124 ]; then
        echo "Time limit exceeded"
    else
        echo "Runtime Error"
    fi
    exit 1
else
    if cmp -s o.out $3;
    then
        echo "AC" > /dev/null
    else
        echo "WA"
        exit 1
    fi
fi
