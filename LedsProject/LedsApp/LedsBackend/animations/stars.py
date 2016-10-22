from ..plugins import Animation, AnimationParameter
import random
import math


class Stars(Animation):

    class Star(object):
        
        def __init__(self, parent, color, startloc, endloc, starMinDuration, starMaxDuration):
            
            self.loc = startloc + int(random.random() * (endloc - startloc))
            done = 0
            while not done:
                self.loc = startloc + int(random.random() * (endloc - startloc))
                done = 1
                for star in parent.theStars:
                    if star.loc == self.loc:
                        done = 0
            self.curTime = 0
            self.duration = (random.random() * (starMaxDuration - starMinDuration)) + starMinDuration
            print("Duration: " + str(self.duration))
            self.red = color[0]
            self.green = color[1]
            self.blue = color[2]

    def __init__(self, id, params):
        super().__init__(id, params)
        self.starCount = params["Star Count"]
        self.brightness = params["Brightness"]
        self.color = params["Color"]
        self.startloc = params["Start Location"]
        self.endloc = params["End Location"]
        self.starMinDuration = params["Star Minimum Duration"]
        self.starMaxDuration = params["Star Maximum Duration"]
        self.theStars = []
        for i in range(self.starCount):
            self.theStars.append(self.Star(self, self.color, self.startloc, self.endloc,
                                           self.starMinDuration, self.starMaxDuration))
            print("Adding star " + str(i))
        
    def animate(self, delta, strip):
        # print "Length: " + str(len(self.theStars))
        toRemove = []
        for star in self.theStars:
            if star.curTime > star.duration:
                toRemove.append(star)
            else:
                brightness = math.sin((star.curTime / float(star.duration)) * math.pi)
                brightness = brightness * self.brightness
                # print str(brightness)
                star.curTime += delta
                # self.strip.setPixelColorWithAlpha(star.loc, star.red, star.green, star.blue, brightness)
                strip.setPixelColor(star.loc, rgb=(int(star.red * brightness), int(star.green * brightness),
                                                   int(star.blue * brightness)))
        for star in toRemove:
            self.theStars.remove(star)
            self.theStars.append(self.Star(self, self.color, self.startloc, self.endloc,
                                           self.starMinDuration, self.starMaxDuration))

    @staticmethod
    def getanimationinfo():
        return {
            "name": "Stars",
            "descriptions": "Pretty twinkling stars"
        }

    @staticmethod
    def getparams():
        return [
            AnimationParameter("Star Count", description="Number of stars", type="integer"),
            AnimationParameter("Brightness", description="Maximum brightness of any individual star",
                               type="float", optional=True, default=1.0, minimum=0.0, maximum=1.0),
            AnimationParameter("Color", description="Color of all of the stars", type="color"),
            AnimationParameter("Star Minimum Duration", type="float", default=1.0, optional=True, advanced=True),
            AnimationParameter("Star Maximum Duration", type="float", default=5.0, optional=True, advanced=True),
            AnimationParameter("Start Location", type="integer"),
            AnimationParameter("End Location", type="integer"),
        ]
