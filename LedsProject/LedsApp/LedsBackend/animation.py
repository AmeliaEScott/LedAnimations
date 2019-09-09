import time
from enum import Enum
import json

animation_classes = []


def animation(animation_display_name, animation_description):
    def animation(animation_class):

        animate_fn = getattr(animation_class, 'animate', None)
        if not callable(animate_fn):
            raise Exception("When using the @animation decorator, you must define an animate function.")

        params = {}

        for name in dir(animation_class):
            if not name.startswith("__"):
                obj = getattr(animation_class, name)
                if type(obj) == AnimationParameter:
                    params[name] = obj
                    obj.name = name

        class NewAnimation:

            parameters = params
            display_name = animation_display_name
            name = animation_class.__name__
            description = animation_description
            metadata = {
                'name': name,
                'displayname': display_name,
                'description': description,
                'parameters': list(sorted([param.as_dict() for param in parameters.values()],
                                          key=lambda x: x['order']))
            }

            def __init__(self, *args, **kwargs):
                self.id = kwargs['id']
                del kwargs['id']
                # Validate parameters
                for param_name, param_metadata in NewAnimation.parameters.items():
                    if param_name not in kwargs:
                        kwargs[param_name] = None
                    kwargs[param_name] = param_metadata.validate(kwargs[param_name])

                self.instance = animation_class(*args, **kwargs)
                self.total_time = 0

            def time_animation(self, *args, **kwargs):
                start = time.time()
                retval = self.instance.animate(*args, **kwargs)
                end = time.time()
                self.total_time += (end - start)
                return retval

            def as_dict(self):
                data = NewAnimation.metadata.copy()
                data['id'] = self.id

                for param_data in data['parameters']:
                    param_data['value'] = getattr(self.instance, param_data['name'], None)

                return data

            def __getattribute__(self, s):
                """
                Passthrough for all other attributes. If the attribute is found in this NewAnimation class,
                it is returned. Otherwise, the attribute is returned from the original class.
                """
                try:
                    return super(NewAnimation, self).__getattribute__(s)
                except AttributeError:
                    pass

                if s == 'animate':
                    return self.time_animation
                else:
                    return self.instance.__getattribute__(s)

        animation_classes.append(NewAnimation)
        return NewAnimation
    return animation


class ParameterError(Exception):
    pass


class ParameterType(Enum):
    """
    INTEGER: A single integer
    FLOAT: A floating point number
    COLOR: A tuple of 3 floats in range [0, 1]
    POSITION: An integer position on the strand
    STRING: A string
    """
    INTEGER = 1,
    FLOAT = 2,
    COLOR = 3,
    POSITION = 4,
    STRING = 5,
    # TODO: Add EXTENT option
    # EXTENT = 6,


class AnimationParameter:

    def __init__(
            self,
            displayname: str,
            param_type: ParameterType,
            description: str = None,
            default=None,
            optional: bool = False,
            advanced: bool = False,
            minimum=None,
            maximum=None,
            order: int = 10000000
    ):
        """
        :param displayname: String that will be shown to the user on the UI
        :param description: Description of what this parameter does. (Optional)
        :param param_type: String that contains either 'integer', 'float', 'color', or 'string'.
        :param default: Default value that will be pre-populated on the UI
        :param optional: Boolean for whether this parameter is mandatory
        :param advanced: Boolean for whether this parameter should be hidden away in an "Advanced" dropdown on the UI
        :param minimum: Minimum value of this parameter. This only applies if 'type' is 'integer' or 'float'
        :param maximum: Maximum value of this parameter. This only applies if 'type' is 'integer' or 'float'
        """
        self.description = description
        self.displayname = displayname
        self.param_type = param_type
        self.default = default
        self.optional = optional
        self.advanced = advanced
        self.minimum = minimum
        self.maximum = maximum
        self.order = order

    def __repr__(self):
        return repr(self.as_dict())

    def as_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'displayname': self.displayname,
            'type': self.param_type.name,
            'default': self.default,
            'optional': self.optional,
            'advanced': self.advanced,
            'minimum': self.minimum,
            'maximum': self.maximum,
            'order': self.order
        }

    def validate(self, value):
        # Get default value
        if self.param_type != ParameterType.STRING and value == '':
            value = None

        if value is None:
            if not self.optional:
                raise ParameterError("'{}' is a required parameter, but was not provided.".format(
                    self.displayname
                ))
            elif self.default is not None:
                value = self.default
            else:
                # No value was provided. But it's optional. But there's no default. So just accept it and return None.
                return None

        # Validate type
        if self.param_type == ParameterType.INTEGER or self.param_type == ParameterType.POSITION:
            # TODO: Treat POSITION parameters special
            try:
                valid = int(value) == float(value)
                value = int(value)
            except ValueError:
                valid = False
            if not valid:
                raise ParameterError("'{}' should be a whole number, but you gave {}.".format(
                    self.displayname, value
                ))
        elif self.param_type == ParameterType.FLOAT:
            try:
                value = float(value)
            except ValueError:
                raise ParameterError("'{}' should be a number, but you gave {}.".format(
                    self.displayname, value
                ))
        elif self.param_type == ParameterType.COLOR:
            if type(value) == str:
                if value.startswith("#"):
                    value = value[1:]
                l = len(value) // 3
                value = list(map(
                    lambda x: int(x, base=16),
                    [value[i:i+l] for i in range(0, len(value), l)]
                ))

            if len(value) != 3:
                raise ParameterError("'{}' should be a tuple of 3 integers, but you gave {}.".format(
                    self.displayname, value
                ))
            try:
                value = tuple(int(x) / 255 for x in value)
            except ValueError:
                raise ParameterError("'{}' should be a tuple of 3 integers, but you gave {}.".format(
                    self.displayname, value
                ))

        # Validate minimum and maximum
        if self.minimum is not None and value < self.minimum:
            raise ParameterError("For '{}', you gave {}, but the minimum allowable value is {}".format(
                self.displayname, value, self.minimum
            ))

        if self.maximum is not None and value > self.maximum:
            raise ParameterError("For '{}', you gave {}, but the maximum allowable value is {}".format(
                self.displayname, value, self.maximum
            ))

        return value