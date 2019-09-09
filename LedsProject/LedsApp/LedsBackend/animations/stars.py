from ..animation import animation, AnimationParameter, ParameterType
import random
import math


@animation("Stars", "Individual twinkling pixels")
class Stars:
    starCount = AnimationParameter(
        "Star Count",
        description="Number of stars",
        param_type=ParameterType.INTEGER,
        default=20,
        minimum=0,
        order=1
    )
    brightness = AnimationParameter(
        "Brightness",
        description="Maximum brightness of any individual star",
        param_type=ParameterType.FLOAT,
        default=1.0,
        minimum=0.0,
        maximum=1.0,
        order=2
    )
    color = AnimationParameter(
        "Color",
        description="Color",
        param_type=ParameterType.COLOR,
        order=3
    )
    starMinDuration = AnimationParameter(
        "Star Minimum Duration, in seconds",
        param_type=ParameterType.FLOAT,
        default=1.0,
        optional=True,
        advanced=True,
        minimum=0,
        order=4
    )
    starMaxDuration = AnimationParameter(
        "Star Maximum Duration, in seconds",
        param_type=ParameterType.FLOAT,
        default=5.0,
        optional=True,
        advanced=True,
        order=5
    )
    startloc = AnimationParameter(
        "Start Location",
        param_type=ParameterType.POSITION,
        advanced=True,
        optional=True,
        default=0,
        minimum=0,
        order=6
    )
    endloc = AnimationParameter(
        "End Location",
        param_type=ParameterType.POSITION,
        advanced=True,
        optional=True,
        minimum=0,
        order=7
    )

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
            # print("Duration: " + str(self.duration))
            self.red = color[0]
            self.green = color[1]
            self.blue = color[2]

    def __init__(self, starCount, brightness, color, startloc, endloc, starMinDuration, starMaxDuration):
        self.starCount = starCount
        self.brightness = brightness
        self.color = color
        self.startloc = startloc
        self.endloc = endloc

        # TODO: Find a better way to pass the strip settings to the animations
        if self.endloc is None:
            self.endloc = 100
        self.starMinDuration = starMinDuration
        self.starMaxDuration = starMaxDuration
        self.theStars = []
        for i in range(self.starCount):
            self.theStars.append(self.Star(self, self.color, self.startloc, self.endloc,
                                           self.starMinDuration, self.starMaxDuration))
            # print("Adding star " + str(i))

    def animate(self, delta, strip):
        if self.endloc is None:
            self.endloc = strip.length

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
                strip.set_pixel_color(star.loc, rgb=(int(star.red * brightness), int(star.green * brightness),
                                                   int(star.blue * brightness)))
        for star in toRemove:
            self.theStars.remove(star)
            self.theStars.append(self.Star(self, self.color, self.startloc, self.endloc,
                                           self.starMinDuration, self.starMaxDuration))
