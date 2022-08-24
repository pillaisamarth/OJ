#!/bin/sh

while read line; do
    for word in $line; do
        inputF="$word.in"
        outputF="$word.out"
        curl "$word.in" > input.in
        curl "$word.out" > output.out
        cpp_ex.sh $1 input.in output.out
        exit_status=$?
        if [ $exit_status -ne 0 ]; then
            exit
        fi
    done
done < "$2"