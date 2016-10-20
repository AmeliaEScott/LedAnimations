try:
    from neopixel import *
except ImportError:
    from ..DummyLibrary import neopixel
from ..LedsBackend.led_strip import LedStrip
from .animations.__init__ import animationclasses
from .plugins import Animation, AnimationParameter
from threading import Thread


class LedSupervisor(Thread):

    def __init__(self, ledstripparams):
        print("Within LED supervisor __init__ now")
        self.strip = LedStrip(**ledstripparams)
        print("successfully initialized LedStrip")
        self.strip.begin()
        print("Successfully called begin() on strip")
        self.animations = {}
        super().__init__()

    def run(self):
        self.strip.show()

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


def test():
    strip = LedStrip(467, 18)
    strip.begin()
    strip.setPixelColor(12, rgb=(255, 255, 0))
