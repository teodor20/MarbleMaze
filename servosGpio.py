import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
pwm=GPIO.PWM(16, 50)
pwm1=GPIO.PWM(18, 50)
pwm.start(6.9)
pwm1.start(6.7)

input("Press Enter to continue...")

pwm.ChangeDutyCycle(5.5)

input("Press Enter to continue...")

pwm.ChangeDutyCycle(6.9)

input("Press Enter to continue...")

pwm.ChangeDutyCycle(7.7)

input("Press Enter to continue...")

pwm.ChangeDutyCycle(6.9)

input("Press Enter to continue...")

pwm.stop()
GPIO.cleanup()