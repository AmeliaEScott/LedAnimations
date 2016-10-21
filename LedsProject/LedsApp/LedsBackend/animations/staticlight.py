from ..plugins import Animation, AnimationParameter


class StaticLight(Animation):
    
    def __init__(self, id, **kwargs):
        super().__init__(id, kwargs)
        self.start = kwargs['start']
        self.end = kwargs['end']
        self.color = kwargs['color']

    def animate(self, delta, strip):
        for i in range(self.start, self.end):
            strip.setPixelColor(i, rgb=self.color)

    @staticmethod
    def getparams():
        return [
            AnimationParameter("start", type="integer"),
            AnimationParameter("end", type="integer"),
            AnimationParameter("color", type="color")
        ]

    @staticmethod
    def getanimationinfo():
        return {
            'name': 'Static Light',
            'description': 'Just a static light along a length of the LED strip'
        }

