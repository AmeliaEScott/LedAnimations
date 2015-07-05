#from ledstrip import NeoPixelWithAlpha
from neopixel import *
from constants import *

class Strobe:
    
    def __init__(self, strip, start, end, on, off, red, green, blue):
        self.strip = strip
        self.start = start
        self.end = end
        self.color = Color(red, green, blue)
        self.on = on
        self.off = off
        self.tick = 0

    def animate(self):
        self.tick += 1
        if self.tick >= (self.on + self.off):
            self.tick = 0
        if self.tick < self.on:
            color = self.color
        else:
            color = Color(0, 0, 0)
        for i in range(self.start, self.end):
            self.strip.setPixelColor(i, color)

