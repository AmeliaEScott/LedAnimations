from ..animation import animation, AnimationParameter, ParameterType
import time
import colorsys

@animation("Cool Rainbow", "It's nice...")
class Rainbow:
    start = AnimationParameter('start', description="Where the rainbow starts",
                       param_type=ParameterType.INTEGER, optional=False)
    end = AnimationParameter('end', description="Where the rainbow ends",
                       param_type=ParameterType.FLOAT, optional=False)
    length = AnimationParameter('length',
                       description="The rainbow will make one trip around the color wheel in this length",
                       param_type=ParameterType.INTEGER, optional=False)
    speed = AnimationParameter('speed', description='How fast to move the colors',
                       param_type=ParameterType.FLOAT, optional=False, default=0)
    brightness = AnimationParameter('brightness', description="Brightness of the whole rainbow (0 to 1)",
                       param_type=ParameterType.FLOAT, default=1, optional=False, minimum=0, maximum=1)
    saturation = AnimationParameter('saturation', description='Saturation (0 to 1)', advanced=True, default=1,
                                    param_type=ParameterType.FLOAT)


    def __init__(self, start, end, length, speed, brightness, saturation):
        self.start = start
        self.end = end
        self.length = length
        self.speed = speed
        self.brightness = brightness
        self.saturation = saturation

        self.tick = 0

    def animate(self, delta, strip):
        self.tick += delta
        hue = self.tick * self.speed
        for i in range(self.start, self.end):
            rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(hue, self.saturation, self.brightness))
            strip.set_pixel_color(i, rgb=tuple(rgb))
            hue = (hue + 1 / self.length) % 1.0
        return