from ..LedsBackend.led_strip import LedStrip
from .animations.__init__ import animationclasses
from .plugins import Animation, AnimationParameter
from threading import Thread
import time
import os
import json

with open(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'settings.json')) as settingsfile:
    settings = json.load(settingsfile)

PIPE_PATH = settings["pipe_name"]


class LedSupervisor(Thread):

    def __init__(self):
        print("Within LED supervisor __init__ now")

        print("successfully initialized LedStrip")
        self.animations = {}
        self.maxid = 0
        super().__init__()
        self.start()

    def run(self):
        try:
            os.mkfifo(PIPE_PATH)
        except OSError:
            print('OSError when opening pipe')
        pipe = open(PIPE_PATH, 'w')
        strip = LedStrip(pipe=pipe, length=settings["strip_settings"]["length"],
                         wraparound=settings["strip_settings"]["wraparound"])

        while True:
            print("Calling self.strip.show()")
            try:
                for anim in self.animations:
                    self.animations[anim].animate(strip)
                strip.show()
                strip.clear()
            except BrokenPipeError:
                print("Pipe broke. Waiting 5 seconds and trying again.")
                time.sleep(5)
            time.sleep(1)

    def addanimation(self, name, options):
        for clazz in animationclasses:
            if clazz.getanimationinfo()['name'] == name:
                self.animations[self.maxid] = clazz(options)
                self.maxid += 1

    @staticmethod
    def getanimationoptions():
        animations = {}
        for clazz in animationclasses:
            # print(repr(clazz))
            # print(repr(clazz.getanimationinfo()))
            classinfo = clazz.getanimationinfo()
            classinfo['parameters'] = []
            for param in clazz.getparams():
                classinfo['parameters'].append(param.__dict__())
            animations[clazz.getanimationinfo()['name']] = classinfo
        return animations
