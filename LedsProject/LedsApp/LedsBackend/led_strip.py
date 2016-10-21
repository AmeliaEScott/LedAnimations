import os


class LedStrip:

    def __init__(self, pipe, length, wraparound=False, powerlimit=None):

        self.length = length

        self.powerLimit = powerlimit
        self.powerUsed = 0

        self.wraparound = wraparound

        self.pixels = [0] * length

        self.pipe = pipe

        print("Finished initializing LED strip")

    def setPixelColor(self, index, color=None, rgb=None, alpha=255, rgba=None):
        print("Setting pixel color...")
        if rgba is not None:
            alpha = rgba[3]
            rgb = rgba[0:3]

        if rgb is not None:
            color = Color(rgb[0], rgb[1], rgb[2])

        if self.wraparound:
            index %= len(self.pixels)
        else:
            if index < 0 or index > len(self.pixels) - 1:
                return

        if color is not None:
            currentcolor = self.pixels[index]
            newcolor = (currentcolor * (1 - (alpha / 255))) + (color * (alpha / 255))
            self.pixels[index] = int(newcolor)
        print("Finished setting pixel color")

    def show(self):
        print("Writing " + repr(self.pixels))
        for pixel in self.pixels:
            self.pipe.write(str(pixel) + " ")
        self.pipe.write("\n")
        self.pipe.flush()


def Color(red, green, blue, white = 0):
    """
    Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    return (white << 24) | (red << 16) | (green << 8) | blue
