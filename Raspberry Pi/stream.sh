# Script to start streaming to PC
#by Brian Do
# https://github.com/bdelta
# https://thenextepoch.blogspot.com/
#!/bin/bash
echo "Please enter ip address of computer:"
read ipaddr
raspivid -vf -hf -n -w 640 -h 480 -o - -t 0 -b 2000000 | nc "$ipaddr" 5000 &
echo "Process ID is: "
echo $!
