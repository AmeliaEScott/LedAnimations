import abc
import json


class Animation:

    @abc.abstractmethod
    def __init__(self, id, options):
        """
        :param options: This will be a dict which contains an entry for every parameter returned by getparams(),
            even if the user did not supply a value. In this case, the value will be None.
            For example, if getparams() returns this:
                [
                    AnimationParameter(displayname='main color', type='color', optional='false'),
                    AnimationParameter(displayname='brightness', type='float', optional='true')
                ]
            Then this __init__() will be called with these parameters:
                {
                    'main color': (123, 12, 47),    # Parameters of type 'color' are actually an rgb triplet
                    'brightness': None,             # This means the user did not provide a 'brightness' value
                }
        """
        self.options = options
        self.id = id
        return

    @abc.abstractmethod
    def animate(self, deltatime, ledstrip):
        """
        This method is called for ever frame of animation. In this method, the animation should
        write all of its pixels for this frame onto the strip
        :param deltatime: The amount of time that has passed since the last time this method was called
        :param ledstrip: The strip to which this animation should write pixels. This will be of type LedStrip
        :return: Nothing
        """
        return

    def tojson(self):
        """
        :return: A JSON String representing this animation in full detail.
        """
        return self.options

    @staticmethod
    @abc.abstractclassmethod
    def getparams():
        """
        This method will be used to construct the user interface for setting up animations.

        :return: Array of AnimationParameter's
        """
        return

    @staticmethod
    @abc.abstractmethod
    def getanimationinfo():
        """
        :return: A dict with a name and description of this animation.
        Example:
        {
            'name': 'Fairy',
            'description': 'Creates a light that continuously moves around the LED strip'
        }
        """
        return


class AnimationParameter:

    def __init__(self, displayname, description=None, type='string', default=None, optional=False, advanced=False,
                 minimum=None, maximum=None):
        """
        :param displayname: String that will be shown to the user on the UI
        :param description: Description of what this parameter does. (Optional)
        :param type: String that contains either 'integer', 'float', 'color', or 'string'.
        :param default: Default value that will be pre-populated on the UI
        :param optional: Boolean for whether this parameter is mandatory
        :param advanced: Boolean for whether this parameter should be hidden away in an "Advanced" dropdown on the UI
        :param minimum: Minimum value of this parameter. This only applies if 'type' is 'integer' or 'float'
        :param maximum: Maximum value of this parameter. This only applies if 'type' is 'integer' or 'float'
        """
        self.description = description
        self.displayname = displayname
        self.type = type
        self.default = default
        self.optional = optional
        self.advanced = advanced
        self.minimum = minimum
        self.maximum = maximum

    def __repr__(self):
        return repr(self.__dict__)

    def __dict__(self):
        return {
            'description': self.description,
            'displayname': self.displayname,
            'type': self.type,
            'default': self.default,
            'optional': self.optional,
            'advanced': self.advanced,
            'minimum': self.minimum,
            'maximum': self.maximum
        }
