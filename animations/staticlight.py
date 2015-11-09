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

    def toJson(self):
        json = '{"animation": "staticLight", "id": "' + self.id + '", "start": '
        json += str(self.start) + ', "end": ' + str(self.end) + ', '
        json += '"red": ' + str(self.red) + ', "green": ' + str(self.green) + ', "blue": ' + str(self.blue) + '}'
        return json

