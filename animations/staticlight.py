#from ledstrip import NeoPixelWithAlpha
from neopixel import *
from constants import *

class StaticLight:
    
    def __init__(self, strip, brightness, start, end):
        self.strip = strip
        self.brightness = brightness
        self.start = start
        self.end = end

    def animate(self):
        color = int(self.brightness * 255)
        for i in range(self.start, self.end):
            self.strip.setPixelColor(i, Color(color, color, color))

