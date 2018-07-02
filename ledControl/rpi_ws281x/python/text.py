#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

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
        if point > 0 and point < (LED_COUNT-1):
            strip.setPixelColor(point, color)
            time.sleep(wait_ms/1000)
    strip.show()

def write(strip, color, text, wait_ms=50):
    formattedText = []
    flatText = []
    counter = 0
    for letter in text:
        formattedText.append([x-(64*counter) for x in letter])
        counter = counter + 1
    formattedText.sort()
    formattedText = formattedText[::-1]
    flatText = [item for sublist in formattedText for item in sublist]

    while flatText[-1] < 63:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0,0,0))
        draw(strip, color, flatText, 0)
        strip.show()
        time.sleep(250/1000.0)
        flatText = [x+8 for x in flatText]


# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    wait_ms = 50
    
    alphabet = [[42, 43, 44, 45, 46, 33, 36, 25, 28, 18, 19, 20, 21, 22],
    [41, 42, 43, 44, 45, 46, 33, 35, 38, 25, 27, 30, 18, 20, 21],
    [42, 43, 44, 45, 33, 38, 25, 30, 18, 21],
    [41, 42, 43, 44, 45, 46, 33, 38, 25, 30, 18, 19, 20, 21],
    [41, 42, 43, 44, 45, 46, 33, 35, 38, 25, 27, 30, 17, 22],
    [41, 42, 43, 44, 45, 46, 33, 35, 25, 27, 17],
    [42, 43, 44, 45, 33, 38, 25, 28, 30, 18, 20, 21],
    [41, 42, 43, 44, 45, 46, 35, 27, 17, 18, 19, 20, 21, 22],
    [41, 46, 33, 34, 35, 36, 37, 38, 25, 26, 27, 28, 29, 30, 17, 22],
    [44, 45, 38, 30, 17, 18, 19, 20, 21],
    [41, 42, 43, 44, 45, 46, 35, 26, 28, 17, 21, 22],
    [41, 42, 43, 44, 45, 46, 38, 30, 22],
    [49, 50, 51, 52, 53, 54, 42, 35, 27, 18, 9, 10, 11, 12, 13, 14],
    [41, 42, 43, 44, 45, 46, 35, 28, 17, 18, 19, 20, 21, 22],
    [42, 43, 44, 45, 33, 38, 25, 30, 18, 19, 20, 21]]
    text = [alphabet[11], alphabet[8], alphabet[11], alphabet[14]]

    try:
        write(strip, Color(0,0,255), text)
    except KeyboardInterrupt:
    	colorWipe(strip, Color(0, 0, 0), 10)
