import pigpio
import time

#Is the pigpio daemon running, e.g.
# does the command pigs t work? Can you start the daemon, e.g. sudo pigpiod?
# Added to startup via "sudo crontab -e"
# Path can be found with "whereis pigpiod"

smallFrame = 23
smallFrameStartPosition = 1430
smallFrameOffset = 400
smallFrameLeftPosition = smallFrameStartPosition - smallFrameOffset
smallFrameRightPosition = smallFrameStartPosition + smallFrameOffset

bigFrame = 24
bigFrameStartPosition = 1550
bigFrameOffset = 450
bigFrameLeftPosition = bigFrameStartPosition - bigFrameOffset - 50
bigFrameRightPosition = bigFrameStartPosition + bigFrameOffset

movementDuration = 0.8

pi = pigpio.pi()

def moveServo(servo, start,end):  #move from start to end, using delta number of seconds
     incMove = (end-start)/100.0
     incTime = movementDuration/100.0
     for x in range(100):
          pi.set_servo_pulsewidth(servo, int(start+x*incMove))
          time.sleep(incTime)

def rotateSmallFrameLeft():
    moveServo(smallFrame, smallFrameStartPosition, smallFrameLeftPosition)
    moveServo(smallFrame, smallFrameLeftPosition, smallFrameStartPosition)

def rotateSmallFrameRight():
    moveServo(smallFrame, smallFrameStartPosition, smallFrameRightPosition)
    moveServo(smallFrame, smallFrameRightPosition, smallFrameStartPosition)

def rotateBigFrameLeft():
    moveServo(bigFrame, bigFrameStartPosition, bigFrameLeftPosition)
    moveServo(bigFrame, bigFrameLeftPosition, bigFrameStartPosition)

def rotateBigFrameRight():
    moveServo(bigFrame, bigFrameStartPosition, bigFrameRightPosition)
    moveServo(bigFrame, bigFrameRightPosition, bigFrameStartPosition)

def start(instructions):
    for instruction in instructions:
        if (instruction == "Up"):
            rotateBigFrameLeft()

        elif(instruction == "Down"):
            rotateBigFrameRight()

        elif(instruction == "Left"):
            rotateSmallFrameLeft()

        elif(instruction == "Right"):
            rotateSmallFrameRight()


def startMotors():
    print(pi.connected)

    if not pi.connected:
        return False

    input("Press Enter to continue...")

    pi.set_servo_pulsewidth(smallFrame, smallFrameStartPosition)
    pi.set_servo_pulsewidth(bigFrame, bigFrameStartPosition)

    time.sleep(0.5)

def stopMotors():
    input("Press Enter to continue...")

    pi.set_servo_pulsewidth(smallFrame, 0)
    pi.set_servo_pulsewidth(bigFrame, 0)

    pi.stop()