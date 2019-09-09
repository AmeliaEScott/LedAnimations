from ..animation import animation, AnimationParameter, ParameterType
import time


@animation("Fairy", "A light that constantly moves around")
class Fairy:
    start = AnimationParameter(
        'Offset',
        description="Location at which this fairy starts",
        param_type=ParameterType.POSITION,
        default=0,
        optional=True,
        advanced=True,
        order=1
    )
    width = AnimationParameter(
        'Size',
        description="Width of the fairy, in number of pixels",
        param_type=ParameterType.INTEGER,
        optional=False,
        order=2
    )
    speed = AnimationParameter(
        'Speed',
        description="Speed of movement, in pixels per second",
        param_type=ParameterType.FLOAT,
        optional=False,
        order=3
    )
    color = AnimationParameter(
        'Color',
        description='Color of the fairy',
        param_type=ParameterType.COLOR,
        optional=False,
        order=4
    )

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
