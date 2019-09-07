# from .animation import Animation, AnimationParameter
# import random
# import math
# import json
#
# DEFAULT_NUM_COSINES = 6
# DEFAULT_FLICKER_SPEED = 30
# DEFAULT_PROPAGATION_SPEED = 3.7
# DEFAULT_BRIGHTNESS_FLICKER_SPEED = 10
# DEFAULT_BRIGHTNESS_EXPONENT = 4.5
# DEFAULT_COLOR_EXPONENT = 0.7
# DEFAULT_MIN_GREEN = 30
# DEFAULT_MAX_GREEN = 100
#
#
# class Fire:
#
#     def __init__(self, id, options):
#         super().__init__(id, options)
#         self.colorFlicker = []
#         self.brightnessFlicker = []
#         self.tick = 0
#         self.maxBrightness = options["Max Brightness"]
#         self.center = options["Center"]
#         self.minStandDev = options["Minimum Width"] / 3
#         self.maxStandDev = options["Maximum Width"] / 3 if options["Maximum Width"] > 0 else self.minStandDev * 1.5
#
#         self.numCosines = options["Number of Cosines"]
#         self.flickerSpeed = options["Flicker Speed"]
#         self.propogationSpeed = options["Propogation Speed"]
#         self.brightnessFlickerSpeed = options["Brightness Flicker Speed"]
#         self.brightnessExponent = options["Brightness Exponent"]
#         self.colorExponent = options["Color Exponent"]
#         self.minGreen = options["Minimum Green"]
#         self.maxGreen = options["Maximum Green"]
#
#         colorFlickers = []
#         brightnessFlickers = []
#         colorSum = 0
#         brightnessSum = 0
#         for i in range(0, self.numCosines):
#             colorFlickers.append(random.random())
#             colorSum += colorFlickers[i]
#             brightnessFlickers.append(random.random())
#             brightnessSum += brightnessFlickers[i]
#         for i in range(0, self.numCosines):
#             colorFlickers[i] /= (colorSum * 2)
#             brightnessFlickers[i] /= (brightnessSum * 2)
#         for i in range(0, self.numCosines):
#             self.colorFlicker.append([colorFlickers[i], random.random()])
#             self.brightnessFlicker.append([brightnessFlickers[i], random.random()])
#
#     def animate(self, delta, strip):
#         self.tick += delta
#         brightness = 0.5
#         for flicker in self.brightnessFlicker:
#             brightness += flicker[0] * math.cos(flicker[1] * self.brightnessFlickerSpeed * self.tick)
#         brightness = brightness**self.brightnessExponent
#         standDev = self.minStandDev + (brightness * (self.maxStandDev - self.minStandDev))
#
#         for i in range(0, int(self.maxStandDev * 3)):
#             timeDiff = i / self.propogationSpeed
#             brightness = self.maxBrightness * math.exp(-(i * i) / (2 * standDev * standDev))
#             # brightness = brightness * math.exp(-(i * i) / (2 * standDev * standDev))
#             color = 0.5
#             for flicker in self.colorFlicker:
#                 color += flicker[0] * math.cos(flicker[1] * self.flickerSpeed * (self.tick - timeDiff))
#             color = color**self.colorExponent
#             red = int(brightness * 255)
#             green = int(brightness * (self.minGreen + color * (self.maxGreen - self.minGreen)))
#             strip.set_pixel_color(self.center + i, rgb=(red, green, 0))
#             strip.set_pixel_color(self.center - i, rgb=(red, green, 0))
#
#     @staticmethod
#     def getanimationinfo():
#         return {
#             'name': 'Fire',
#             'description': 'It sort of looks like fire, I guess'
#         }
#
#     @staticmethod
#     def getparams():
#         return [
#             AnimationParameter("Max Brightness", description="Maximum brightness, on scale of 0 to 1",
#                                type="float", default=1.0, optional=True, minimum=0, maximum=1),
#             AnimationParameter("Center", description="Location of center of fire on the LED strip",
#                                type="integer", optional=False),
#             AnimationParameter("Minimum Width", type="float", optional=False, minimum=0),
#             AnimationParameter("Maximum Width", type="float", optional=True, default=0, minimum=0),
#             AnimationParameter("Number of Cosines", type="integer", default=DEFAULT_NUM_COSINES,
#                                optional=True, advanced=True),
#             AnimationParameter("Flicker Speed", type="float", default=DEFAULT_NUM_COSINES,
#                                optional=True, advanced=True),
#             AnimationParameter("Propogation Speed", type="float", default=DEFAULT_PROPAGATION_SPEED,
#                                optional=True, advanced=True),
#             AnimationParameter("Brightness Flicker Speed", type="float", default=DEFAULT_BRIGHTNESS_FLICKER_SPEED,
#                                optional=True, advanced=True),
#             AnimationParameter("Brightness Exponent", type="float", default=DEFAULT_BRIGHTNESS_EXPONENT,
#                                optional=True, advanced=True),
#             AnimationParameter("Color Exponent", type="float", default=DEFAULT_COLOR_EXPONENT,
#                                optional=True, advanced=True),
#             AnimationParameter("Minimum Green", type="integer", default=DEFAULT_MIN_GREEN,
#                                optional=True, advanced=True),
#             AnimationParameter("Maximum Green", type="integer", default=DEFAULT_MAX_GREEN,
#                                optional=True, advanced=True)
#         ]
