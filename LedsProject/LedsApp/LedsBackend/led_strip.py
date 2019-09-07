import numpy as np
import zmq
import colorsys


class LedStrip:

    def __init__(self, zmq_port, length, wraparound=False, power_limit=None):

        self.length = length
        self.power_limit = power_limit
        self.wraparound = wraparound

        self.pixels = np.zeros([length, 3], dtype=np.float32)

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:{}".format(zmq_port))

        print("Finished initializing LED strip")

    def set_pixel_color(self, index, rgb=None, rgba=None, hsv=None, hsva=None):
        alpha = 1.0

        if hsv is not None:
            rgb = colorsys.hsv_to_rgb(*hsv)

        if hsva is not None:
            rgb = colorsys.hsv_to_rgb(*hsv[0:3])
            alpha = hsva[3]

        if rgba is not None:
            rgb = rgba[0:3]
            alpha = rgba[3]

        if rgb is None:
            raise Exception("No color provided")

        if self.wraparound:
            index %= len(self.pixels)
        elif index < 0 or index > self.pixels.shape[0] - 1:
            raise IndexError("Index {} is out of range (0, {})".format(index, self.pixels.shape[0] - 1))

        color = np.array(rgb, dtype=np.float32)
        self.pixels[index] = (self.pixels[index] * (1 - alpha)) + alpha * color

    def show(self):
        self.socket.send(self.pixels)

    def clear(self):
        self.pixels[:, :] = 0.0
