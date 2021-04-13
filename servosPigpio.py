import time

import pigpio

#Is the pigpio daemon running, e.g.
# does the command pigs t work? Can you start the daemon, e.g. sudo pigpiod?

smallFrame = 23
bigFrame = 24

pi = pigpio.pi()
print(pi.connected)

input("Press Enter to continue...")

#The starting positions of the servos can be seen below.
#Less than 1450/1550 will rotate to the LEFT
#More than 1450/1550 will rotate to the RIGHT

pi.set_servo_pulsewidth(smallFrame, 1450)
pi.set_servo_pulsewidth(bigFrame, 1550)

input("Press Enter to continue...")

pi.set_servo_pulsewidth(smallFrame, 1300)

input("Press Enter to continue...")

pi.set_servo_pulsewidth(smallFrame, 1450)

input("Press Enter to continue...")

pi.set_servo_pulsewidth(bigFrame, 1750)

input("Press Enter to continue...")

pi.set_servo_pulsewidth(bigFrame, 1450)

input("Press Enter to continue...")

# switch servo off
pi.set_servo_pulsewidth(smallFrame, 0)
pi.set_servo_pulsewidth(bigFrame, 0)

pi.stop()