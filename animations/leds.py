from stars import Stars
from staticlight import StaticLight
from constants import *
from ledstrip import NeoPixelWithAlpha
import time

print LED_COUNT
#millis = lambda: int(round(time.time() * 1000))

ticks = 0

# Create NeoPixel object with appropriate configuration.
strip = NeoPixelWithAlpha(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

stars = Stars(strip, 30, 1, 255, 0, 0)
#150-225
light = StaticLight(strip, 1, 150, 225)
absoluteStart = time.time()

while 1:
    start = time.time()
    light.animate()
    stars.animate()
    #light.animate()
    strip.show()
    ticks += 1
    sleepTime = 0.033 - (time.time() - start)
    if(sleepTime < 0):
        sleepTime = 0
    time.sleep(sleepTime)

absoluteEnd = time.time()
print "Ticks per second: " + str(ticks / (absoluteEnd - absoluteStart))
