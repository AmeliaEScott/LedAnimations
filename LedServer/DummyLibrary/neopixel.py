

class Adafruit_NeoPixel:

    def __init__(self, length, pin, freq_hz=800000, dma=5, invert=False):
        self.length = length
        self.pin = pin
        print("WARNING: You're using the dummy library!!")

    def setPixelColor(self, index, color):
        pass

    def numPixels(self):
        return self.length

    def setPixelColorRGB(self, index, red, green, blue):
        pass

    def getPixelColor(self, index):
        return 0

    def show(self):
        pass

    def begin(self):
        pass


def Color(red, green, blue):
    return 0
