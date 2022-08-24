#!/bin/sh

g++ $1 2> /dev/null
exit_status=$?
if [ $exit_status -ne 0 ]; then
    echo "Compilation Error" > verdict.txt
    exit 1
fi
timeout 5s ./a.out 1> o.out 2> /dev/null < $2
exit_status=$?
if [ $exit_status != 0 ]; then
    if [ $exit_status -eq 124 ]; then
        echo "Time limit exceeded" > verdict.txt
    else
        echo "Runtime Error" > verdict.txt
    fi
    exit 1
else
    if cmp -s o.out $3;
    then
        echo "AC" > verdict.txt
    else
        echo "WA" > verdict.txt
        exit 1
    fi
fi
