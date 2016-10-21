

class Adafruit_NeoPixel:

    def __init__(self, length, pin, freq_hz=800000, dma=5, invert=False, brightness=255):
        self.length = length
        self.pin = pin
        self.pixels = [0] * length
        print("WARNING: You're using the dummy library!!")

    def setPixelColor(self, index, color):
        self.pixels[index] = color

    def numPixels(self):
        return self.length

    def setPixelColorRGB(self, index, red, green, blue):
        pass

    def getPixelColor(self, index):
        return self.pixels[index]

    def show(self):
        print("Dummy strip: " + repr(self.pixels))

    def begin(self):
        pass

    def __del__(self):
        print("Deleting dummy LED strip")
        del self.pixels
        del self.pin
        del self.length


def Color(red, green, blue):
    return 0
