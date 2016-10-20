from neopixel import *
from constants import *

class WrapAroundStrip(Adafruit_NeoPixel):

    def setPixelColor(self, index, color):
        index = index % LED_COUNT
        super(WrapAroundStrip, self).setPixelColor(index, color)
