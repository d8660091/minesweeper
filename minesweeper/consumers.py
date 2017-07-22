from channels.generic.websockets import JsonWebsocketConsumer
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels import Group
import json

from .models import Game, GameData


@receiver(post_save, sender=GameData)
def send_update(sender, instance, **kwargs):
    game_id = str(instance.pk)
    game = Game()
    game.load(game_id)
    Group(game_id).send({
        "text": json.dumps({
            'type': 'game_change',
            'data': game.get_user_map().tolist(),
        })
    })


class GameConsumer(JsonWebsocketConsumer):
    """Game server which handles websockets."""

    # channel_session = True
    # strict_ordering = True

    def handle_request(self, request, data):
        if request == 'reveal':
            return self.game.get_user_map().tolist()

    def connection_groups(self, **kwargs):
        return ['test']

    def connect(self, message, **kwargs):
        self.message.reply_channel.send({"accept": True})
        Group(kwargs['game_id']).add(message.reply_channel)
        game = Game()
        game.load(kwargs['game_id'])
        game.new(16, 16, 40)
        game.save()

    def receive(self, content, **kwargs):
        game = Game()
        game.load(kwargs['game_id'])
        if content['type'] == 'reveal':
            x = content['data']['x']
            y = content['data']['y']
            if game.reveal(x, y):
                pass
            else:
                game.save()
        elif content['type'] == 'mark':
            x = content['data']['x']
            y = content['data']['y']
            game.mark(x, y)
            game.save()

    def disconnect(self, message, **kwargs):
        Group(kwargs['game_id']).discard(message.reply_channel)
