#from ledstrip import NeoPixelWithAlpha
from neopixel import *
from constants import *

class Fairy:
    
    def __init__(self, strip, start, width, speed, red, green, blue):
        self.strip = strip
        self.start = start
        self.width = width
        self.speed = speed
        self.red = red
        self.blue = blue
        self.green = green

        self.tick = 0

    def animate(self):
        self.tick += 1
        dist = ((self.tick * self.speed) + self.start) % LED_COUNT
        fraction = dist - (int(dist))
        dist = int(dist)
        #fraction = fraction ** 0.5
        startFraction = 1 - fraction
        for i in range(1, int(self.speed) + 2) if int(self.speed) > 1 else range(int(self.speed) - self.width, self.width):
            self.strip.setPixelColor(dist - i, 0)
        self.strip.setPixelColor(dist, Color(int(startFraction * self.red), int(startFraction * self.green), int(startFraction * self.blue)))
        for i in range(1, self.width):
            self.strip.setPixelColor(dist + i, Color(self.red, self.green, self.blue))
        self.strip.setPixelColor(dist + self.width, Color(int(fraction * self.red), int(fraction * self.green), int(fraction * self.blue)))
