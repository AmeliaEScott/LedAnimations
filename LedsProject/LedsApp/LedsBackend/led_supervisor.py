from .led_strip import LedStrip
from .animation import animation_classes
# This import is not unused. I need to import all of the animation modules to populate the 'animation_classes' list.
from .animations import *
from threading import Thread
import time
import os
import json


print("===animations===")
print([cls.__name__ for cls in animation_classes])


with open(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'settings.json')) as settingsfile:
    settings = json.load(settingsfile)

ZMQ_PORT = settings["zmq_port"]


class LedSupervisor(Thread):
    """
    This class runs a separate thread that handles animations. The bulk of the important code
    is in the run() method.
    """

    def __init__(self):
        self.animations = {}
        self.maxid = 0
        super().__init__()
        self.running = True
        self.start()

    def run(self):
        time.sleep(5)

        strip = LedStrip(ZMQ_PORT, length=settings["strip_settings"]["length"],
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
                    time.sleep(delay)
            except RuntimeError:
                print("Caught a runtime error in LedSupervisor. Probably because of multithreading, but who knows?")
                time.sleep(0.01)

    def addanimation(self, name, options):
        try:
            cls = next(filter(lambda x: x.name == name, animation_classes))
        except StopIteration:
            raise Exception("No animation found with name {}".format(name))

        print(options)
        new_animation = cls(id=self.maxid, **options)
        self.animations[self.maxid] = new_animation
        self.maxid += 1
        return new_animation.as_dict()

    def getanimations(self):
        return self.animations

    def getanimationsjson(self):
        output = {}
        for id in sorted(self.animations.keys()):
            output[id] = {
                "name": self.animations[id].name,
                "options": self.animations[id].options,
                "id": id
            }
        return output

    def removeanimation(self, id):
        del self.animations[id]

    def stop(self):
        self.running = False

    @staticmethod
    def getanimationoptions():
        return {
            cls.name: cls.metadata for cls in animation_classes
        }
