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
            'game_ended': game.game_ended,
            'data': game.get_user_map().tolist(),
        })
    })


class GameConsumer(JsonWebsocketConsumer):
    """Game server which handles websockets."""

    # channel_session = True
    # strict_ordering = True

    def connection_groups(self, **kwargs):
        return ['test']

    def connect(self, message, **kwargs):
        self.message.reply_channel.send({"accept": True})
        Group(kwargs['game_id']).add(message.reply_channel)
        game = Game()
        game.load(kwargs['game_id'])
        game.save()

    def receive(self, content, **kwargs):
        game = Game()
        game.load(kwargs['game_id'])
        if content['type'] == 'reveal':
            x = content['data']['x']
            y = content['data']['y']
            game.reveal(x, y)
            if game.game_ended:
                game.save()
            else:
                game.save()
        elif content['type'] == 'mark':
            x = content['data']['x']
            y = content['data']['y']
            game.mark(x, y)
            game.save()
        elif content['type'] == 'reveal_multiple':
            points = content['data']['points']
            for point in points:
                game.reveal(point['x'], point['y'])
            game.save()
        elif content['type'] == 'restart':
            w = content['data'].get('w', 16)
            h = content['data'].get('h', 16)
            mines_total = content['data'].get('mines_total', 40)
            game.new(w, h, mines_total)
            game.save()

    def disconnect(self, message, **kwargs):
        Group(kwargs['game_id']).discard(message.reply_channel)
