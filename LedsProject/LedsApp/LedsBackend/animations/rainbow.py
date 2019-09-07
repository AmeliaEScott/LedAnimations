# from .animation import Animation, AnimationParameter
# import time
# import colorsys
#
#
# class Rainbow:
#
#     def __init__(self, id, options):
#         super().__init__(id, options=options)
#         self.start = options['start']
#         self.end = options['end']
#         self.length = options['length']
#         self.speed = options['speed']
#         self.brightness = options['brightness']
#         self.saturation = options['saturation']
#
#         self.tick = 0
#
#     def animate(self, delta, strip):
#         self.tick += delta
#         hue = self.tick * self.speed
#         for i in range(self.start, self.end):
#             rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(hue, self.saturation, self.brightness))
#             strip.set_pixel_color(i, rgb=tuple(rgb))
#             hue = (hue + 1 / self.length) % 1.0
#         return
#
#     @staticmethod
#     def getparams():
#         return [
#             AnimationParameter('start', description="Where the rainbow starts",
#                                type='integer', optional=False),
#             AnimationParameter('end', description="Where the rainbow ends",
#                                type='float', optional=False),
#             AnimationParameter('length',
#                                description="The rainbow will make one trip around the color wheel in this length",
#                                type='integer', optional=False),
#             AnimationParameter('speed', description='How fast to move the colors',
#                                type='float', optional=False, default=0),
#             AnimationParameter('brightness', description="Brightness of the whole rainbow (0 to 1)",
#                                type='float', default=1, optional=False),
#             AnimationParameter('saturation', description='Saturation (0 to 1)', advanced=True, default=1, type='float')
#         ]
#
#     @staticmethod
#     def getanimationinfo():
#         return {
#             'name': 'Rainbow',
#             'description': 'A rainbow that optionally moves'
#         }
