#!/bin/bash
#Script to start streaming from Rpi to PC
#by Brian Do
# https://github.com/bdelta
# https://thenextepoch.blogspot.com/
if [ -p fifo264 ]
then
	rm fifo264
fi
mkfifo fifo264
nc -l -v -p 5000 > fifo264 &
last=$!
gnome-terminal -- "./stream_test"
sleep 3
kill $last
nc -l -v -p 5000 > fifo264
