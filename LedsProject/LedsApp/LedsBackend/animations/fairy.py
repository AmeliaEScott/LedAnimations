from ..animation import animation, AnimationParameter, ParameterType
import time


@animation("Fairy", "A light that constantly moves around")
class Fairy:
    start = AnimationParameter('Offset', description="Location at which this fairy starts",
                               param_type=ParameterType.POSITION, default=0, optional=True)
    width = AnimationParameter('width', description="Width of the fairy, in number of pixels",
                               param_type=ParameterType.INTEGER, optional=False)
    speed = AnimationParameter('speed', description="Speed of movement, in pixels per second",
                               param_type=ParameterType.FLOAT, optional=False)
    color = AnimationParameter('color', description='Color of the fairy',
                               param_type=ParameterType.COLOR, optional=False)

    def __init__(self, start, width, speed, color):
        print("MY COLOR IS ({}): {}".format(type(color), color))
        self.start = start
        self.width = width
        self.speed = speed
        self.color = color
        self.tick = time.time()

    def animate(self, delta, strip):
        self.tick += delta
        dist = ((self.tick * self.speed) + self.start)
        fraction = dist - (int(dist))
        dist = int(dist)
        strip.set_pixel_color(dist, rgba=self.color + (1.0 - fraction,))
        for i in range(1, self.width):
            strip.set_pixel_color(dist + i, rgb=self.color)
        strip.set_pixel_color(dist + self.width, rgba=self.color + (fraction,))

    @staticmethod
    def getparams():
        return [

        ]

    @staticmethod
    def getanimationinfo():
        return {
            'name': 'Fairy',
            'description': 'A light that moves continously around the LED strip'
        }
