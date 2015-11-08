
from animations.stars import Stars
from animations.staticlight import StaticLight
from neopixel import *
from animations.fire import Fire
from animations.strobe import Strobe
from animations.fairy import Fairy
from constants import *
from wraparoundstrip import WrapAroundStrip
from threading import Lock
import time

class Leds(object):

    animations=[]
    lock = Lock()
    def __init__(self):
        # Create NeoPixel object with appropriate configuration.
        strip = WrapAroundStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        strip.begin()

        while 1:
            start = time.time()
            with lock:
                for anim in self.animations:
                    anim.animate()
            strip.show()
            sleepTime = 0.033 - (time.time() - start)
            if(sleepTime < 0):
                sleepTime = 0
            time.sleep(sleepTime)
    
    def remove(self, id):
        with lock:
            for anim in animations:
                if(anim.id == id):
                    animations.remove(anim)
