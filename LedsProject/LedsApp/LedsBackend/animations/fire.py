from ..animation import animation, AnimationParameter, ParameterType
import random
import math

DEFAULT_NUM_COSINES = 6
DEFAULT_FLICKER_SPEED = 30
DEFAULT_PROPAGATION_SPEED = 3.7
DEFAULT_BRIGHTNESS_FLICKER_SPEED = 10
DEFAULT_BRIGHTNESS_EXPONENT = 4.5
DEFAULT_COLOR_EXPONENT = 0.7
DEFAULT_MIN_GREEN = 0.1
DEFAULT_MAX_GREEN = 0.4


@animation("Flickery Fire", "Nice flickery boi")
class Fire:
    maxBrightness = AnimationParameter(
        "Brightness",
        description="Brightness, on scale of 0 to 1",
        param_type=ParameterType.FLOAT,
        default=1.0,
        optional=True,
        minimum=0,
        maximum=1,
        order=1
    )
    center = AnimationParameter(
        "Center",
        description="Location of center of fire on the LED strip",
        param_type=ParameterType.POSITION,
        optional=False,
        order=2
    )
    minWidth = AnimationParameter(
        "Minimum Width",
        param_type=ParameterType.FLOAT,
        optional=True,
        minimum=0,
        advanced=True,
        order=4
    )
    maxWidth = AnimationParameter(
        "Maximum Width",
        ParameterType.FLOAT,
        optional=False,
        minimum=0,
        order=3
    )
    numCosines = AnimationParameter(
        "Number of Cosines",
        ParameterType.INTEGER,
        default=DEFAULT_NUM_COSINES,
        optional=True,
        advanced=True,
        minimum=0
    )
    flickerSpeed = AnimationParameter(
        "Flicker Speed",
        ParameterType.FLOAT,
        default=DEFAULT_NUM_COSINES,
        optional=True,
        advanced=True,
        minimum=0
    )
    propogationSpeed = AnimationParameter(
        "Propogation Speed",
        ParameterType.FLOAT,
        default=DEFAULT_PROPAGATION_SPEED,
        optional=True,
        advanced=True,
        minimum=0
    )
    brightnessFlickerSpeed = AnimationParameter(
        "Brightness Flicker Speed",
        ParameterType.FLOAT,
        default=DEFAULT_BRIGHTNESS_FLICKER_SPEED,
        optional=True,
        advanced=True,
        minimum=0
    )
    brightnessExponent = AnimationParameter(
        "Brightness Exponent",
        ParameterType.FLOAT,
        default=DEFAULT_BRIGHTNESS_EXPONENT,
        optional=True,
        advanced=True
    )
    colorExponent = AnimationParameter(
        "Color Exponent",
        ParameterType.FLOAT,
        default=DEFAULT_COLOR_EXPONENT,
        optional=True,
        advanced=True
    )
    minGreen = AnimationParameter(
        "Minimum Green",
        param_type=ParameterType.FLOAT,
        default=DEFAULT_MIN_GREEN,
        optional=True,
        advanced=True,
        minimum=0,
        maximum=1
    )
    maxGreen = AnimationParameter(
        "Maximum Green",
        param_type=ParameterType.FLOAT,
        default=DEFAULT_MAX_GREEN,
        optional=True,
        advanced=True,
        minimum=0,
        maximum=1
    )

    def __init__(self, maxBrightness, center, minWidth, maxWidth, numCosines, flickerSpeed, propogationSpeed,
                 brightnessFlickerSpeed, brightnessExponent, colorExponent, minGreen, maxGreen):
        self.colorFlicker = []
        self.brightnessFlicker = []
        self.tick = 0
        self.maxBrightness = maxBrightness
        self.center = center
        self.maxStandDev = maxWidth / 3
        self.minStandDev = minWidth / 3 if minWidth is not None else self.maxStandDev / 1.5
        self.maxWidth = maxWidth
        self.minWidth = minWidth

        self.numCosines = numCosines
        self.flickerSpeed = flickerSpeed
        self.propogationSpeed = propogationSpeed
        self.brightnessFlickerSpeed = brightnessFlickerSpeed
        self.brightnessExponent = brightnessExponent
        self.colorExponent = colorExponent
        self.minGreen = minGreen
        self.maxGreen = maxGreen

        colorFlickers = []
        brightnessFlickers = []
        colorSum = 0
        brightnessSum = 0
        for i in range(0, self.numCosines):
            colorFlickers.append(random.random())
            colorSum += colorFlickers[i]
            brightnessFlickers.append(random.random())
            brightnessSum += brightnessFlickers[i]
        for i in range(0, self.numCosines):
            colorFlickers[i] /= (colorSum * 2)
            brightnessFlickers[i] /= (brightnessSum * 2)
        for i in range(0, self.numCosines):
            self.colorFlicker.append([colorFlickers[i], random.random()])
            self.brightnessFlicker.append([brightnessFlickers[i], random.random()])



    def animate(self, delta, strip):
        self.tick += delta
        brightness = 0.5
        for flicker in self.brightnessFlicker:
            brightness += flicker[0] * math.cos(flicker[1] * self.brightnessFlickerSpeed * self.tick)
        brightness = brightness**self.brightnessExponent
        standDev = self.minStandDev + (brightness * (self.maxStandDev - self.minStandDev))

        for i in range(0, int(self.maxStandDev * 3)):
            timeDiff = i / self.propogationSpeed
            brightness = self.maxBrightness * math.exp(-(i * i) / (2 * standDev * standDev))
            # brightness = brightness * math.exp(-(i * i) / (2 * standDev * standDev))
            color = 0.5
            for flicker in self.colorFlicker:
                color += flicker[0] * math.cos(flicker[1] * self.flickerSpeed * (self.tick - timeDiff))
            color = color**self.colorExponent
            red = brightness
            green = brightness * (self.minGreen + color * (self.maxGreen - self.minGreen))
            strip.set_pixel_color(self.center + i, rgb=(red, green, 0))
            strip.set_pixel_color(self.center - i, rgb=(red, green, 0))
