#!/bin/sh

javac $1.java

java $1 < $2 > out.txt