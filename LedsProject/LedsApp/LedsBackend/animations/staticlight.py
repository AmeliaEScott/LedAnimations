# from .animation import Animation, AnimationParameter
#
#
# class StaticLight:
#
#     def __init__(self, id, options):
#         super().__init__(id, options)
#         self.start = options['start']
#         self.end = options['end']
#         self.color = options['color']
#
#     def animate(self, delta, strip):
#         for i in range(self.start, self.end):
#             strip.set_pixel_color(i, rgb=self.color)
#
#     @staticmethod
#     def getparams():
#         return [
#             AnimationParameter("start", type="integer"),
#             AnimationParameter("end", type="integer"),
#             AnimationParameter("color", type="color")
#         ]
#
#     @staticmethod
#     def getanimationinfo():
#         return {
#             'name': 'Static Light',
#             'description': 'Just a static light along a length of the LED strip'
#         }
#
