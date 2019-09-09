from ..animation import animation, AnimationParameter, ParameterType


@animation("Static Light", "A stationary solid-color light")
class StaticLight:

    start = AnimationParameter(
        "Beginning",
        description="Location of beginning of light",
        param_type=ParameterType.POSITION,
        default=0,
        optional=True,
        minimum=0,
        order=1
    )
    end = AnimationParameter(
        "End",
        description="Location of end of light (leave blank to fill all lights)",
        param_type=ParameterType.POSITION,
        optional=True,
        minimum=0,
        order=2
    )
    color = AnimationParameter(
        "Color",
        description="Color of light",
        param_type=ParameterType.COLOR,
        optional=False,
        order=3
    )

    def __init__(self, start, end, color):
        self.start = start
        self.end = end
        self.color = color

    def animate(self, delta, strip):
        if self.end is None:
            self.end = strip.length

        strip.pixels[self.start:self.end, :] = self.color
