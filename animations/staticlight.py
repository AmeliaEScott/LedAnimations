#from ledstrip import NeoPixelWithAlpha
from neopixel import *
from constants import *

class StaticLight:
    
    def __init__(self, strip, start, end, red, green, blue):
        self.strip = strip
        self.start = start
        self.end = end
        self.red = red
        self.blue = blue
        self.green = green

    def animate(self):
        for i in range(self.start, self.end):
            self.strip.setPixelColor(i, Color(self.red, self.green, self.blue))

