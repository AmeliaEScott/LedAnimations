try:
    from neopixel import *
except ImportError:
    from ..DummyLibrary.neopixel import *


class LedStrip(Adafruit_NeoPixel):

    def __init__(self, length, pin, freq_hz=800000, dma=5, invert=False, wraparound=False, powerlimit=None):
        super().__init__(length, pin, freq_hz, dma, invert)

        self.powerLimit = powerlimit
        self.powerUsed = 0

        self.wraparound = wraparound

        print("Finished initializing LED strip")

    def setPixelColor(self, index, color=None, rgb=None, alpha=255, rgba=None):
        print("Setting pixel color...")
        if rgba is not None:
            alpha = rgba[3]
            rgb = rgba[0:3]

        if rgb is not None:
            color = Color(rgb[0], rgb[1], rgb[2])

        if self.wraparound:
            index = index % self.numPixels()
        else:
            if index < 0 or index > self.numPixels() - 1:
                return

        if color is not None:
            currentcolor = self.getPixelColor(index)
            newcolor = (currentcolor * (1 - (alpha / 255))) + (color * (alpha / 255))
            super().setPixelColor(index, newcolor)
        print("Finished setting pixel color")
