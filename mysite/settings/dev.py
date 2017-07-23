import os
from .common import * # noqa
from .common import BASE_DIR

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "mysite.routing.channel_routing",
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
