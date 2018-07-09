#!/usr/bin/env python3
import time
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 64      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    #Wipe color across display a pixel at a time.
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def draw(strip, color, points, wait_ms=50):
    for point in points:
        strip.setPixelColor(point, color)
        time.sleep(wait_ms/1000)
    strip.show()


# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    wait_ms = 50

    #icon with structure: [[color,ledIDs],[color,ledIDs]] 
    cloud = [[Color(255, 255, 255),[1, 2, 8, 9, 10, 11, 16, 17, 18, 19, 24, 
        25, 26, 27, 32, 33, 34, 35, 40, 41, 42, 
        43, 48, 49, 50, 51, 57, 58]]]

    shower_rain = [cloud[0],[Color(0, 0, 255), [21, 23, 37, 39, 53, 55]]]
    rain = [20, 21, 22, 23, 36, 37, 38, 39, 52, 53, 54, 55]

    clear_sky = [0,3,7,9,14,19,20,26,27,28,29,31,
        32,34,35,36,37,43,44,49,54,56,60,63]
    
    try:
        """
        draw(strip, Color(255, 255, 255), cloud)
        time.sleep(5)
        colorWipe(strip, Color(0, 0, 0), 10)
        draw(strip, Color(255, 255, 0), sun)
        time.sleep(5)
        colorWipe(strip, Color(0, 0, 0), 10)
        draw(strip, Color(255, 255, 255), cloud)
        draw(strip, Color(0, 0, 255), lightRain)
        time.sleep(5)
        colorWipe(strip, Color(0, 0, 0), 10)
        draw(strip, Color(255, 255, 255), cloud)
        draw(strip, Color(0, 0, 255), heavyRain)
        time.sleep(5)
        colorWipe(strip, Color(0, 0, 0), 10)"""
        print(cloud)
        print(shower_rain)
    except KeyboardInterrupt:
    	colorWipe(strip, Color(0, 0, 0), 10)
