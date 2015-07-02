from constants import *
from neopixel import *
import random
import math

NUM_COSINES = 6

class Fire(object):
    
    colorFlicker = []
    brightnessFlicker = []

    def __init__(self, strip, center, brightness, minWidth, maxWidth):
        self.strip = strip
        self.brightness = brightness
        self.center = center
        self.minWidth = minWidth
        self.maxWidth = maxWidth
        colorFlickers = []
        brightnessFlickers = []
        colorSum = 0
        brightnessSum = 0
        for i in range(0, NUM_COSINES):
            colorFlickers.append(random.random())
            colorSum += colorFlickers[i]
            brightnessFlickers.append(random.random())
            brightnessSum += brightnessFlickers[i]
        for i in range(0, NUM_COSINES):
            colorFlickers[i] = colorFlickers[i] / colorSum
            brightnessFlickers[i] = brightnessFlickers[i] / brightnessSum
        for i in colorFlickers:
            print i
        
    def animate(self):
        self.strip.setPixelColor(star.loc, Color(r, g, b))
