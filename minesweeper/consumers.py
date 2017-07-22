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
            'data': game.game_map.tolist(),
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
        game.new(5, 5, 5)
        game.save()

    def receive(self, content, **kwargs):
        print(content)

    def disconnect(self, message, **kwargs):
        Group(kwargs['game_id']).discard(message.reply_channel)
