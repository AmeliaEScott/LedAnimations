from ..animation import animation, AnimationParameter, ParameterType
import colorsys


@animation("Rainbow", "Rainbow that optionally moves")
class Rainbow:
    # TODO: Change to ParameterType.EXTENT
    start = AnimationParameter(
        'Beginning',
        description="Where the rainbow starts",
        param_type=ParameterType.INTEGER,
        optional=False,
        minimum=0,
        order=1
    )
    end = AnimationParameter(
        'End',
        description="Where the rainbow ends",
        param_type=ParameterType.FLOAT,
        optional=False,
        minimum=0,
        order=2
    )
    length = AnimationParameter(
        'Scale',
        description="The rainbow will make one trip around the color wheel in this length",
        param_type=ParameterType.INTEGER,
        optional=True,
        advanced=True,
        minimum=0,
        order=3
    )
    speed = AnimationParameter(
        'Speed',
        description='How fast to move the colors, in pixels / second',
        param_type=ParameterType.FLOAT,
        optional=True,
        default=0,
        order=4
    )
    brightness = AnimationParameter(
        'Brightness',
        description="Brightness of the whole rainbow (0 to 1)",
        param_type=ParameterType.FLOAT,
        default=1,
        optional=False,
        minimum=0,
        maximum=1,
        order=5
    )
    saturation = AnimationParameter(
        'Saturation',
        description='Saturation (0 to 1)',
        advanced=True,
        default=1,
        param_type=ParameterType.FLOAT,
        minimum=0,
        maximum=1,
        order=6
    )

    def __init__(self, start, end, length, speed, brightness, saturation):
        self.start = start
        self.end = end
        if length is None:
            length = end - start
        self.length = length
        self.speed = speed
        self.brightness = brightness
        self.saturation = saturation

        self.tick = 0

    def animate(self, delta, strip):
        self.tick += delta
        hue = self.tick * self.speed
        for i in range(self.start, self.end):
            rgb = colorsys.hsv_to_rgb(hue, self.saturation, self.brightness)
            strip.set_pixel_color(i, rgb=tuple(rgb))
            hue = (hue + 1 / self.length) % 1.0
