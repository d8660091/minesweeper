from .common import * # noqa

DEBUG = False

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "ROUTING": "mysite.routing.channel_routing",
        "CONFIG": {
            "hosts": [('redis', 6379)],
        },
    },
}

ALLOWED_HOSTS = [
    "web",
    "127.0.0.1",
]

STATIC_ROOT = '/static'
