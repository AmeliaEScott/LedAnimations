from stars import Stars
from staticlight import StaticLight
from fire import Fire
from constants import *
#from ledstrip import NeoPixelWithAlpha
from neopixel import *
import time

print LED_COUNT
#millis = lambda: int(round(time.time() * 1000))

ticks = 0

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

stars = Stars(strip, 15, 1, 255, 255, 255)
#150-225
#light = StaticLight(strip, 150, 225, 255, 40, 0)
light = StaticLight(strip, 0, LED_COUNT, 63, 12, 0)
fire = Fire(strip, 140, 1, 5, 10)
absoluteStart = time.time()
totalSleepTime = 0
for i in range(0, 300):
#while 1:
    start = time.time()
    #light.animate()
    #stars.animate()
    #light.animate()
    fire.animate()
    strip.show()
    ticks += 1
    sleepTime = 0.033 - (time.time() - start)
    if(sleepTime < 0):
        sleepTime = 0
    totalSleepTime += sleepTime
    time.sleep(sleepTime)

absoluteEnd = time.time()
print "Ticks per second: " + str(ticks / (absoluteEnd - absoluteStart))
print "Proportion spent sleeping: " + str(totalSleepTime / (absoluteEnd - absoluteStart))
