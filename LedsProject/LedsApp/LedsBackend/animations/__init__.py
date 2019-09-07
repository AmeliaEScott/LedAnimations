from os.path import dirname, basename, isfile, join, splitext
import glob
from importlib import import_module

__all__ = list(
    map(
        lambda x: splitext(basename(x))[0],
        filter(
            lambda x: isfile(x) and not x.endswith('__init__.py'),
            glob.glob(join(dirname(__file__), "*.py"))
        )
    )
)
#
# for modulename in __all__:
#     module = import_module("." + modulename, __name__)
