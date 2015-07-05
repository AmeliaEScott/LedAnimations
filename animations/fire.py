from constants import *
from neopixel import *
import random
import math

NUM_COSINES = 6
FLICKER_SPEED = 0.6
PROPAGATION_SPEED = 3.7
BRIGHTNESS_FLICKER_SPEED = 0.6
BRIGHTNESS_EXPONENT = 4.5
COLOR_EXPONENT = 0.7
MIN_GREEN = 30
MAX_GREEN = 100

class Fire(object):
    
    def __init__(self, strip, maxBrightness, center, minStandDev, maxStandDev):
        self.colorFlicker = []
        self.brightnessFlicker = []
        self.tick = 0
        self.strip = strip
        self.maxBrightness = maxBrightness
        self.center = center
        self.minStandDev = minStandDev
        self.maxStandDev = maxStandDev
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
            colorFlickers[i] = colorFlickers[i] / (colorSum * 2)
            brightnessFlickers[i] = brightnessFlickers[i] / (brightnessSum * 2)
        for i in range(0, NUM_COSINES):
            self.colorFlicker.append([colorFlickers[i], random.random()])
            self.brightnessFlicker.append([brightnessFlickers[i], random.random()])
    def animate(self):
        self.tick += 1
        tick = self.tick
        brightness = 0.5
        for flicker in self.brightnessFlicker:
            brightness += flicker[0] * math.cos(flicker[1] * BRIGHTNESS_FLICKER_SPEED * self.tick)
        brightness = brightness**BRIGHTNESS_EXPONENT
        standDev = self.minStandDev + (brightness * (self.maxStandDev - self.minStandDev))
        
        for i in range(0, int(self.maxStandDev * 3)):
            timeDiff = i / PROPAGATION_SPEED
            brightness = self.maxBrightness * math.exp(-(i * i) / (2 * standDev * standDev))
            #brightness = brightness * math.exp(-(i * i) / (2 * standDev * standDev))
            color = 0.5
            for flicker in self.colorFlicker:
                color += flicker[0] * math.cos(flicker[1] * FLICKER_SPEED * (self.tick - timeDiff))
            color = color**COLOR_EXPONENT
            red = int(brightness * 255)
            green = int(brightness * (MIN_GREEN + color * (MAX_GREEN - MIN_GREEN)))
            self.strip.setPixelColor(self.center + i, Color(red, green, 0))
            self.strip.setPixelColor(self.center - i, Color(red, green, 0))
