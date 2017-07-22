from channels.generic.websockets import JsonWebsocketConsumer
from django.db.models.signals import post_save
from .models import Game, GameData


class GameConsumer(JsonWebsocketConsumer):
    """Game server which handles websockets."""

    # channel_session = True
    # strict_ordering = True

    def get_game_change_callback(self, game_id):
        def game_change_callback(sender, **kwargs):
            if kwargs['instance'].pk == int(game_id):
                game = Game()
                game.load(game_id)
                self.send({
                    'type': 'game_change',
                    'data': game.game_map.tolist(),
                })
        return game_change_callback

    def handle_request(self, request, data):
        if request == 'reveal':
            return self.game.get_user_map().tolist()

    def connection_groups(self, **kwargs):
        return ['test']

    def connect(self, message, **kwargs):
        callback = self.get_game_change_callback(kwargs['game_id'])
        post_save.connect(callback, sender=GameData)
        self.message.reply_channel.send({"accept": True})
        game = Game()
        game.load(kwargs['game_id'])
        game.new(5, 5, 5)
        game.save()

    def receive(self, content, **kwargs):
        pass

    def disconnect(self, message, **kwargs):
        pass
