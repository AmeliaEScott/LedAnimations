try:
    from neopixel import *
except ImportError:
    from .dummy_neopixel import *
import os
import time
import json
import signal
import sys


with open(os.path.join(os.path.dirname(__file__), '..', 'settings.json')) as settingsfile:
    settings = json.load(settingsfile)

PIPE_PATH = settings["pipe_name"]

LED_COUNT = settings["strip_settings"]["length"]
LED_PIN = settings["strip_settings"]["pin"]
LED_FREQ_HZ = settings["strip_settings"]["frequency"]
LED_DMA = settings["strip_settings"]["dma"]
LED_BRIGHTNESS = settings["strip_settings"]["brightness"]
LED_INVERT = settings["strip_settings"]["invert"]


class LedServer:

    def __init__(self):
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        strip.begin()

        try:
            os.mkfifo(PIPE_PATH)
        except OSError:
            print("OSError while making pipe")

        # pipe = open(PIPE_PATH, 'r')
        self.running = True

        signal.signal(signal.SIGINT, self.end)

        with open(PIPE_PATH, 'r') as pipe:
            while self.running:
                result = pipe.readline().split(" ")
                if result is None or len(result) <= 1 or result == "":
                    print("Broken pipe. Waiting 5 seconds then trying again.")
                    time.sleep(5)
                else:
                    for i in range(0, len(result) - 1):
                        strip.setPixelColor(i, int(result[i]))
                    strip.show()
        print("Done cleaning up!")

    def end(self, signal, frame):
        self.running = False


LedServer()
