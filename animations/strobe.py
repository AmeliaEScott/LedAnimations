#from ledstrip import NeoPixelWithAlpha
from neopixel import *
from constants import *

class Strobe:
    
    def __init__(self, strip, start, end, on, off, red, green, blue):
        self.strip = strip
        self.start = start
        self.end = end
        self.color = Color(red, green, blue)
        self.red = red
        self.green = green
        self.blue = blue
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

    def toJson(self):
        json = '{"animation": "strobe", "start": '
        json += str(self.start) + ', "end": ' + str(self.end) + ', "on": ' + str(self.on) +  ', "off": ' + str(self.off) + ', '
        json += '"red": ' + str(self.red) + ', "green": ' + str(self.green) + ', "blue": ' + str(self.blue) + '}'
        return json

