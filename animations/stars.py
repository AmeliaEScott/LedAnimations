from constants import *
from neopixel import *
import random
import math

#Min and max duration, in ticks. (30 tick/sec I guess)
starMinDuration = 30
starMaxDuration = 150

class Stars(object):
    
    theStars=[]
    
    class Star(object):
        
        def __init__(self, parent, red, green, blue):
            
            self.loc = int(random.random() * LED_COUNT)
            done = 0
            while(not(done)):
                self.loc = int(random.random() * LED_COUNT)
                done = 1
                for star in parent.theStars:
                    if(star.loc == self.loc):
                        done = 0
            self.curTime = 0
            self.duration = int(random.random() * (starMaxDuration - starMinDuration)) + starMinDuration
            self.red = red
            self.green = green
            self.blue = blue
            #self.red = int(random.random() * 255)
            #self.green = int(random.random() * 255)
            #self.blue = int(random.random() * 255)

    def __init__(self, strip, starCount, brightness, red, green, blue):
        self.strip = strip
        self.starCount = starCount
        self.brightness = brightness
        for i in range(starCount):
            self.theStars.append(self.Star(self, red, green, blue))
        self.red = red
        self.green = green
        self.blue = blue
        
    def animate(self):
        toRemove = []
        for star in self.theStars:
            if(star.curTime > star.duration):
                toRemove.append(star)
            else:
                brightness = math.sin((star.curTime / float(star.duration)) * math.pi)
                brightness = brightness * self.brightness
                #print str(brightness)
                star.curTime += 1
                #self.strip.setPixelColorWithAlpha(star.loc, star.red, star.green, star.blue, brightness)
                self.strip.setPixelColor(star.loc, Color(int(star.red * brightness), int(star.green * brightness), int(star.blue * brightness)))
        for star in toRemove:
            self.theStars.remove(star)
            self.theStars.append(self.Star(self, self.red, self.green, self.blue))
                
    def toJson(self):
        json = '{"animation": "stars", "starCount": ' + str(self.starCount) + ', "brightness": ' + str(self.brightness) + ', '
        json += '"red": ' + str(self.red) + ', "green": ' + str(self.green) + ', "blue": ' + str(self.blue) + '}'
        return json

    
