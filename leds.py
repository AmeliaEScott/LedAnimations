
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
    strip = WrapAroundStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    lock = Lock()
    maxId = 0

    def __init__(self):
        self.animations.append(Fire(self.strip, 1, 250, 15, 20))
        self.animations.append(Strobe(self.strip, 0, LED_COUNT, 1, 1, 255, 255, 255))
        self.animations.append(Fairy(self.strip, 430, 50, 10.5, 255, 180, 0))

        
    def run(self):
        # Create NeoPixel object with appropriate configuration.
        #strip = WrapAroundStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

        while 1:
            start = time.time()
            with self.lock:
                for anim in self.animations:
                    anim.animate()
            self.strip.show()
            sleepTime = 0.033 - (time.time() - start)
            if(sleepTime < 0):
                sleepTime = 0
            time.sleep(sleepTime)
    
    def remove(self, id):
        with self.lock:
            for anim in animations:
                if(anim.id == id):
                    animations.remove(anim)

    def add(self, anim):
        with self.lock:
            anim.id = self.id;
            self.id = self.id + 1;
            self.animations.append(anim)
