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
    "159.203.53.11",
    "minesweeper.xudeng.io",
]

STATIC_ROOT = '/static'
