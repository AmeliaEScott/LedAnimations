try:
    from neopixel import *
except ImportError:
    from DummyLibrary.neopixel import *
from LedsBackend.led_strip import LedStrip

def test():
    strip = LedStrip(467, 18)
    strip.begin()
    strip.setPixelColor(12, rgb=(255, 255, 0))