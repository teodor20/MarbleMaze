import time

import pigpio

#Is the pigpio daemon running, e.g.
# does the command pigs t work? Can you start the daemon, e.g. sudo pigpiod?

pi = pigpio.pi()
print(pi.connected)

input("Press Enter to continue...")

pi.set_servo_pulsewidth(23, 1450)
pi.set_servo_pulsewidth(24, 1550) #big frame #low - left #high - right

input("Press Enter to continue...")

pi.set_servo_pulsewidth(23, 1300)

input("Press Enter to continue...")

pi.set_servo_pulsewidth(23, 1450)

input("Press Enter to continue...")

pi.set_servo_pulsewidth(24, 1750)

input("Press Enter to continue...")

pi.set_servo_pulsewidth(24, 1450)

input("Press Enter to continue...")

# switch servo off
pi.set_servo_pulsewidth(23, 0)
pi.set_servo_pulsewidth(24, 0)

pi.stop()