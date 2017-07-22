from minesweeper import consumers
from channels import route_class

channel_routing = [
    route_class(consumers.GameConsumer, path=r"^/minesweeper/stream/(?P<session_id>[^/]+)")
]
