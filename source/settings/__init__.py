try:
    from settings.local import *
except ImportError:
    from settings.production import *
