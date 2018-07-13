import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

def button_callback(channel):
    #global time_stamp       # put in to debounce  
    #time_now = time.time()  
    #if (time_now - time_stamp) >= 0.3:  
    #    print("pressed")  
    #time_stamp = time_now
    print("Pressed")
#GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
#time_stamp = time.time()

GPIO.add_event_detect(23,GPIO.FALLING,callback=button_callback, bouncetime = 300) # Setup event on pin 10 rising edge
raw_input("Press enter to quit\n") # Run until someone presses enter
GPIO.cleanup()

#GPIO.cleanup() # Clean up
#GPIO.setmode(GPIO.BCM)

#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#while True:
#    input_state = GPIO.input(23)
#    if input_state == False:
#        print('Button Pressed')
#        time.sleep(0.2)
