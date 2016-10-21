# try:
#     from neopixel import *
# except ImportError:
#     from .DummyLibrary.neopixel import *
import os
import time

PIPE_PATH = '/Users/Timmy/git/LedAnimations/datapipe'

# LED_COUNT      = 16      # Number of LED pixels.
# LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
# LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
# LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
# LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
#
# strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# strip.begin()

try:
    os.mkfifo(PIPE_PATH)
except OSError:
    print("OSError while making pipe")

pipe = open(PIPE_PATH, 'r')

while True:
    result = bytearray(pipe.readline(), 'ascii')
    if result is None or len(result) <= 0:
        print("Broken pipe. Waiting 5 seconds then trying again.")
        time.sleep(5)
    else:
        for i in range(0, len(result) - 1):
            print(result[i])

    print('Done reading, for now...')
