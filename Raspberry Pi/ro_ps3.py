# Raspberry Pi Script to interface ps3 controller + servo control
#by Brian Do
# https://github.com/bdelta
# https://thenextepoch.blogspot.com/

import RPi.GPIO as gpio
import time
import pygame
import serial

#Motor driver interfacing
#11, 12 = left wheels | 13, 15 = right wheels
def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(11, gpio.OUT)
    gpio.setup(12, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)

def MotorOff():
    gpio.output(11, False)
    gpio.output(12, False)
    gpio.output(13, False)
    gpio.output(15, False)

def forward():
    gpio.output(11, True) #IN4
    gpio.output(12, False) #IN3
    gpio.output(13, True) #IN2
    gpio.output(15, False) #IN1

def reverse():
    gpio.output(11, False)
    gpio.output(12, True)
    gpio.output(13, False)
    gpio.output(15, True)

def fleft():
    gpio.output(11, False)
    gpio.output(12, False)
    gpio.output(13, True)
    gpio.output(15, False)

def fright():
	gpio.output(11, True)
	gpio.output(12, False)
	gpio.output(13, False)
	gpio.output(15, False)

def bleft():
    gpio.output(11, False)
    gpio.output(12, False)
    gpio.output(13, False)
    gpio.output(15, True)

def bright():
    gpio.output(11, False)
    gpio.output(12, True)
    gpio.output(13, False)
    gpio.output(15, False)

def rot_right():
    gpio.output(11, True)
    gpio.output(12, False)
    gpio.output(13, False)
    gpio.output(15, True)

def rot_left():
    gpio.output(11, False)
    gpio.output(12, True)
    gpio.output(13, True)
    gpio.output(15, False)


#Script start
init()

#Servo Control
ser = serial.Serial('/dev/ttyUSB0', 115200)
ser.flushInput()
print(ser.name)

# Settings for JoyBorg
axisUpDown = 1                          # Joystick axis to read for up / down position
axisLeftRight = 0                       # Joystick axis to read for left / right position
camera = 3                              # Camera & Distance Pan Axis
interval = 0.1                          # Time between keyboard updates in seconds, smaller responds faster but uses more processor time
o_button = 1 							# Mapping of button
thresh = 0.5

# Setup pygame and key states
hadEvent = True
moveQuit = False
moveUp, moveDown, rotLeft, rotRight = False, False, False, False
forwardLeft, forwardRight, backLeft, backRight = False, False, False, False
camLeft, camRight = False, False
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()


# Function to handle pygame events
def PygameHandler(events):
    # Variables accessible outside this function
    global hadEvent, moveQuit
    global moveUp, moveDown, rotLeft, rotRight
    global forwardLeft, forwardRight, backLeft, backRight
    global camLeft, camRight
    # Handle each event individually
    for event in events:
        if event.type == pygame.JOYBUTTONDOWN:
            # A key has been pressed, see if it is one we want
            hadEvent = True
            if joystick.get_button(o_button) == 1:
                moveQuit = True
        elif event.type == pygame.JOYAXISMOTION:
            # A joystick has been moved, read axis positions (-1 to +1)
            moveUp, moveDown, rotLeft, rotRight = False, False, False, False
            forwardLeft, forwardRight, backLeft, backRight = False, False, False, False
            camLeft, camRight = False, False
            hadEvent = True
            upDown = joystick.get_axis(axisUpDown)
            leftRight = joystick.get_axis(axisLeftRight)
            servo = joystick.get_axis(camera)
            # 8 Axis Control
            # Forward and backwards
            if leftRight > -thresh and leftRight < thresh:
                if upDown < -thresh:
                    moveUp = True
                elif upDown > thresh:
                    moveDown = True
            # Left and right
            if upDown > -thresh and upDown < thresh:
                if leftRight < -thresh:
                    rotLeft = True
                elif leftRight > thresh:
                    rotRight = True

            #FRight and FLeft
            if upDown < -thresh:
                if leftRight > thresh:
                    forwardRight = True
                elif leftRight < -thresh:
                    forwardLeft = True
            elif upDown > thresh:
                if leftRight > thresh:
                    backRight = True
                elif leftRight < -thresh:
                    backLeft = True

            if servo > thresh:
                camRight = True
            elif servo < -thresh:
                camLeft = True
try:
    print 'Press O on controller to quit'
    # Loop indefinitely
    while True:
        # Get the currently pressed keys on the keyboard
        PygameHandler(pygame.event.get())
        if hadEvent:
            # Keys have changed, generate the command list based on keys
            hadEvent = False
            if moveQuit:
                break
            elif rotLeft:
                rot_left()
            elif rotRight:
                rot_right()
            elif forwardLeft:
                fleft()
            elif forwardRight:
                fright()
            elif backLeft:
                bleft()
            elif backRight:
                bright()
            elif moveUp:
                forward()
            elif moveDown:
            	reverse()
            else:
                MotorOff()
                
            if camRight:
                ser.write(b'r')
            elif camLeft:
                ser.write(b'l')
            
        # Wait for the interval period
        time.sleep(interval)
    # Disable all drives
    MotorOff()
except KeyboardInterrupt:
    # CTRL+C exit, disable all drives
    MotorOff()

gpio.cleanup()
ser.close()