from __future__ import print_function, division
# try:
#     from neopixel import *
#     import _rpi_ws281x as ws
# except ImportError:
#     from .dummy_neopixel import *
import os
import time
import json
import signal
import sys
import zmq
import numpy as np


with open(os.path.join(os.path.dirname(__file__), '..', 'settings.json')) as settingsfile:
    settings = json.load(settingsfile)

PIPE_PATH = settings["pipe_name"]
ZMQ_PORT = settings["zmq_port"]
LED_COUNT = settings["strip_settings"]["length"]
LED_PIN = settings["strip_settings"]["pin"]
LED_FREQ_HZ = settings["strip_settings"]["frequency"]
LED_DMA = settings["strip_settings"]["dma"]
LED_BRIGHTNESS = settings["strip_settings"]["brightness"]
LED_INVERT = settings["strip_settings"]["invert"]
strip_type = settings["strip_settings"]["type"].lower()
# types = {
#     'rgb': ws.WS2811_STRIP_RGB,
#     'rbg': ws.WS2811_STRIP_RBG,
#     'grb': ws.WS2811_STRIP_GRB,
#     'gbr': ws.WS2811_STRIP_GBR,
#     'brg': ws.WS2811_STRIP_BRG,
#     'bgr': ws.WS2811_STRIP_BGR,
# }
# STRIP_TYPE = types[strip_type]

running = True


def end(*args, **kwargs):
    global running
    running = False


signal.signal(signal.SIGINT, end)

context = zmq.Context()
socket = context.socket(zmq.SUB)
print("ZMQ Port: {}".format(ZMQ_PORT))
socket.setsockopt(zmq.SUBSCRIBE, "")
socket.connect("tcp://127.0.0.1:{}".format(ZMQ_PORT))
socket.subscribe("")


strip = Adafruit_NeoPixel(
    num=LED_COUNT,
    pin=LED_PIN,
    freq_hz=LED_FREQ_HZ,
    dma=LED_DMA,
    invert=LED_INVERT,
    brightness=LED_BRIGHTNESS,
    strip_type=STRIP_TYPE
)
strip.begin()

two_fifty_five = np.ones([LED_COUNT, 3], np.float32) * 255

while running:
    result = socket.poll(500)
    if result == 0:
        continue
    else:
        print("Receiving a thing")
    msg = socket.recv(copy=False, )

    # Assume incoming data is numpy array of floats in range (0, 1)
    data = np.frombuffer(msg, dtype=np.float32)
    data = np.reshape(data, [-1, 3])

    # Convert to integers in range (0, 255)
    data = (data * two_fifty_five).astype(np.int32)

    # Convert to the form that the LED strip needs: a 32-bit integer
    data_packed = (data[:, 0] << 16) | (data[:, 1] << 8) | (data[:, 2])

    # TODO: Is there a more efficient way to copy over the colors?
    for i in range(0, data_packed.shape[0]):
        strip.setPixelColor(i, data_packed[i])

print("Done cleaning up!")
