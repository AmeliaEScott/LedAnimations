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
    """
    This class runs a separate thread that handles animations. The bulk of the important code
    is in the run() method.
    """

    def __init__(self):
        print("Within LED supervisor __init__ now")

        print("successfully initialized LedStrip")
        self.animations = {}
        self.maxid = 0
        super().__init__()
        self.running = True
        self.start()

    def run(self):
        time.sleep(5)
        try:
            os.mkfifo(PIPE_PATH)
        except OSError:
            print('OSError when opening pipe')
        pipe = open(PIPE_PATH, 'w')
        strip = LedStrip(pipe=pipe, length=settings["strip_settings"]["length"],
                         wraparound=settings["strip_settings"]["wraparound"])

        framelength = 1 / settings["misc"]["framerate"]
        starttime = time.time()
        while self.running:
            previoustime = starttime
            starttime = time.time()
            # print("Calling self.strip.show()")
            try:
                for anim in self.animations:
                    self.animations[anim].animate(delta=starttime - previoustime, strip=strip)
                strip.show()
                strip.clear()
                delay = framelength - (time.time() - starttime)
                if delay > 0:
                    pass
                    time.sleep(delay)
            except BrokenPipeError:
                print("Pipe broke. Waiting 5 seconds and trying again.")
                time.sleep(5)
            except RuntimeError:
                print("Caught a runtime error in LedSupervisor. Probably because of multithreading, but who knows?")
                time.sleep(0.01)
            # time.sleep(1)

    def addanimation(self, name, options):
        for clazz in animationclasses:
            if clazz.getanimationinfo()['name'] == name:
                self.animations[self.maxid] = clazz(self.maxid, options)
                self.maxid += 1

    def getanimations(self):
        return self.animations

    def removeanimation(self, id):
        del self.animations[id]

    def stop(self):
        self.running = False

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
