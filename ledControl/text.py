#!/usr/bin/env python3

import time
from neopixel import *
import sys

#sys.path.append('.:build/lib.linux-armv7l-2.7')

# LED strip configuration:
LED_COUNT      = 64      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

alphabet = {'A':[42, 43, 44, 45, 46, 33, 36, 25, 28, 18, 19, 20, 21, 22],
    'B':[41, 42, 43, 44, 45, 46, 33, 35, 38, 25, 27, 30, 18, 20, 21],
    'C':[42, 43, 44, 45, 33, 38, 25, 30, 18, 21],
    'D':[41, 42, 43, 44, 45, 46, 33, 38, 25, 30, 18, 19, 20, 21],
    'E':[41, 42, 43, 44, 45, 46, 33, 35, 38, 25, 27, 30, 17, 22],
    'F':[41, 42, 43, 44, 45, 46, 33, 35, 25, 27, 17],
    'G':[42, 43, 44, 45, 33, 38, 25, 28, 30, 18, 20, 21],
    'H':[41, 42, 43, 44, 45, 46, 35, 27, 17, 18, 19, 20, 21, 22],
    'I':[41, 33, 25, 34, 35, 36, 37, 38, 46, 30],
    'J':[44, 45, 38, 30, 17, 18, 19, 20, 21],
    'K':[41, 42, 43, 44, 45, 46, 35, 26, 28, 17, 21, 22],
    'L':[41, 42, 43, 44, 45, 46, 38, 30, 22],
    'M':[49, 50, 51, 52, 53, 54, 42, 35, 27, 18, 9, 10, 11, 12, 13, 14],
    'N':[41, 42, 43, 44, 45, 46, 35, 28, 17, 18, 19, 20, 21, 22],
    'O':[42, 43, 44, 45, 33, 38, 25, 30, 18, 19, 20, 21],
    'P':[41, 33, 25, 18, 19, 28, 36, 44, 43, 42, 45, 46],
    'Q':[42, 33, 25, 18, 19, 20, 21, 45, 44, 43, 38, 30, 22, 14],
    'R':[46, 45, 44, 22, 21, 28, 36, 19, 18, 25, 33, 41, 42, 43],
    'S':[38, 30, 21, 45, 28, 35, 42, 33, 25, 18],
    'T':[41, 33, 25, 17, 49, 34, 35, 36, 37, 38],
    'U':[46, 38, 30, 22, 21, 20, 19, 18, 17, 41, 42, 43, 44, 45],
    'V':[38, 30, 21, 45, 20, 19, 18, 17, 41, 42, 43, 44],
    'W':[46, 30, 37, 36, 53, 52, 51, 50, 18, 19, 20, 21, 17, 49],
    'X':[41, 42, 17, 18, 27, 35, 44, 45, 46, 20, 21, 22],
    'Y':[49, 50, 17, 18, 43, 27, 36, 37, 38],
    'Z':[46, 38, 30, 22, 45, 36, 27, 18, 17, 25, 33, 41]}


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

def stringToList(text):
    output = []
    #toDo: implement also lower case letter and remove this
    text = text.upper()
    for letter in text:
        if letter in alphabet:
            output.append(alphabet[letter])
        else:
            #append questionmark
            print("unknown symbol {}".format(letter))
    return output

def write(strip, color, text, wait_ms=50):
    textList = stringToList(text)
    formattedText = []
    flatText = []
    counter = 0
    for letter in textList:
        formattedText.append([x-(64*counter) for x in letter])
        counter = counter + 1
    
    #flatten the text lists to one list
    flatText = [item for sublist in formattedText for item in sublist]
    #sort the text list
    flatText.sort()
    #reverse text list
    flatText = flatText[::-1]    

    
    while flatText[-1] < 63:
        #clear screen
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0,0,0))
        #draw the current text list
        draw(strip, color, flatText, 0)
        strip.show()
        time.sleep(250/1000.0)
        #move text 1 coloumn to the left
        flatText = [x+8 for x in flatText]
    
    #clear screen
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()


# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    wait_ms = 50
    
    try:
        write(strip, Color(0,0,255), "LILO")
    except KeyboardInterrupt:
    	colorWipe(strip, Color(0, 0, 0), 10)
