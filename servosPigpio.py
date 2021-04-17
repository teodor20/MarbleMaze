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
bigFrameLeftPosition = bigFrameStartPosition - bigFrameOffset
bigFrameRightPosition = bigFrameStartPosition + bigFrameOffset

movementDuration = 0.8
sleepDuration = 0

pi = pigpio.pi()

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

def start(instructions):
    print(pi.connected)

    if not pi.connected:
        return False

    input("Press Enter to continue...")

    pi.set_servo_pulsewidth(smallFrame, smallFrameStartPosition)
    pi.set_servo_pulsewidth(bigFrame, bigFrameStartPosition)

    input("Press Enter to continue...")

    for instruction in instructions:
        if (instruction == "Up"):
            rotateBigFrameLeft()

        elif(instruction == "Down"):
            rotateBigFrameRight()

        elif(instruction == "Left"):
            rotateSmallFrameLeft()

        elif(instruction == "Right"):
            rotateSmallFrameRight()

        time.sleep(1)


    input("Press Enter to continue...")

    pi.set_servo_pulsewidth(smallFrame, 0)
    pi.set_servo_pulsewidth(bigFrame, 0)

    pi.stop()