import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

def button_callback(channel):
    print("Pressed")
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 23 to be an input pin and set initial value to be pulled low (off)


GPIO.add_event_detect(23,GPIO.FALLING,callback=button_callback, bouncetime = 300) # Setup event on pin 23 rising edge
raw_input("Press enter to quit\n") # Run until someone presses enter
GPIO.cleanup()