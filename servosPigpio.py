import pigpio
import time

#Is the pigpio daemon running, e.g.
# does the command pigs t work? Can you start the daemon, e.g. sudo pigpiod?
# Added to startup via "sudo crontab -e"
# Path can be found with "whereis pigpiod"

smallFrame = 23
smallFrameStartPosition = 1450
smallFrameLeftPosition = 1000
smallFrameRightPosition = 1900

bigFrame = 24
bigFrameStartPosition = 1550
bigFrameLeftPosition = 1100
bigFrameRightPosition = 2000

movementDuration = 1.5
sleepDuration = 1

def moveServo(servo, start,end):  #move from start to end, using delta number of seconds
     incMove = (end-start)/100.0
     incTime = movementDuration/100.0
     for x in range(100):
          pi.set_servo_pulsewidth(servo, int(start+x*incMove))
          time.sleep(incTime)

def rotateSmallFrameLeft():
    moveServo(smallFrame, smallFrameStartPosition, smallFrameLeftPosition)
    time.sleep(sleepDuration)
    moveServo(smallFrame, smallFrameLeftPosition, smallFrameStartPosition)

def rotateSmallFrameRight():
    moveServo(smallFrame, smallFrameStartPosition, smallFrameRightPosition)
    time.sleep(sleepDuration)
    moveServo(smallFrame, smallFrameRightPosition, smallFrameStartPosition)

def rotateBigFrameLeft():
    moveServo(bigFrame, bigFrameStartPosition, bigFrameLeftPosition)
    time.sleep(sleepDuration)
    moveServo(bigFrame, bigFrameLeftPosition, bigFrameStartPosition)

def rotateBigFrameRight():
    moveServo(bigFrame, bigFrameStartPosition, bigFrameRightPosition)
    time.sleep(sleepDuration)
    moveServo(bigFrame, bigFrameRightPosition, bigFrameStartPosition)


pi = pigpio.pi()
print(pi.connected)

input("Press Enter to continue...")

#The starting positions of the servos can be seen below.
#Less than 1450/1550 will rotate to the LEFT
#More than 1450/1550 will rotate to the RIGHT

pi.set_servo_pulsewidth(smallFrame, smallFrameStartPosition)
pi.set_servo_pulsewidth(bigFrame, bigFrameStartPosition)

input("Press Enter to continue...")

rotateSmallFrameLeft()
time.sleep(1)
rotateBigFrameLeft()
time.sleep(1)
rotateSmallFrameRight()
time.sleep(1)
rotateBigFrameRight()

input("Press Enter to continue...")

# switch servo off
pi.set_servo_pulsewidth(smallFrame, 0)
pi.set_servo_pulsewidth(bigFrame, 0)

pi.stop()