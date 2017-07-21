from channels.generic.websockets import JsonWebsocketConsumer


class GameConsumer(JsonWebsocketConsumer):

    # strict_ordering = True

    def connection_groups(self, **kwargs):
        return ['test']

    def connect(self, message, **kwargs):
        self.message.reply_channel.send({"accept": True})

    def receive(self, content, **kwargs):
        self.send(content)

    def disconnect(self, message, **kwargs):
        pass
