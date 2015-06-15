from neopixel import *


def getColor(rgb):
    Blue =  rgb & 255
    Green = (rgb >> 8) & 255
    Red =   (rgb >> 16) & 255
    return (Red, Green, Blue)

class NeoPixelWithAlpha(Adafruit_NeoPixel):

    def setPixelColorWithAlpha(self, index, red, green, blue, alpha):
        color = getColor(self.getPixelColor(index))
        newRed = int(red * alpha) + int(color[0] * (1-alpha))
        newGreen = int(green * alpha) + int(color[1] * (1-alpha))
        newBlue = int(blue * alpha) + int(color[2] * (1-alpha))
        self.setPixelColor(index, Color(newRed, newGreen, newBlue))
