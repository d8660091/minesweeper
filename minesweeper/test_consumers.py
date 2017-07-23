# from channels import Group
from channels.test import ChannelTestCase, WSClient, apply_routes
from .consumers import GameConsumer

import numpy as np
import json


class ConsumersTests(ChannelTestCase):
    def test_game_server(self):
        client = WSClient()

        with apply_routes([GameConsumer.as_route(path=r"^/minesweeper/stream/(?P<game_id>[^/]+)")]):
            client.send_and_consume('websocket.connect', path='/minesweeper/stream/1')
            user_map = np.array(client.receive()['data'])
            self.assertEqual(client.receive()['type'], 'game_change')
            self.assertTrue(np.array_equal(user_map, np.full(user_map.shape, -2)))

            client.send_and_consume('websocket.receive',
                                    text=json.dumps({
                                        'type': 'reveal',
                                        'data': {
                                            'x': 0,
                                            'y': 0,
                                        }
                                    }),
                                    path='/minesweeper/stream/1')
            self.assertEqual(client.receive()['type'], 'game_change')

            client.send_and_consume('websocket.receive',
                                    text=json.dumps({
                                        'type': 'mark',
                                        'data': {
                                            'x': 0,
                                            'y': 0,
                                        }
                                    }),
                                    path='/minesweeper/stream/1')
            self.assertEqual(client.receive()['type'], 'game_change')

            client.send_and_consume('websocket.receive',
                                    text=json.dumps({
                                        'type': 'restart',
                                        'data': {
                                            'x': 0,
                                            'y': 0,
                                        }
                                    }),
                                    path='/minesweeper/stream/1')
            self.assertEqual(client.receive()['type'], 'game_change')

    def test_game_server_for_multiplayers(self):
        client1 = WSClient()
        client2 = WSClient()
        with apply_routes([GameConsumer.as_route(path=r"^/minesweeper/stream/(?P<game_id>[^/]+)")]):
            client1.send_and_consume('websocket.connect', path='/minesweeper/stream/1')

            client2.send_and_consume('websocket.connect', path='/minesweeper/stream/1')
            self.assertEqual(client1.receive()['type'], 'game_change')

            client2.send_and_consume('websocket.receive',
                                     text=json.dumps({
                                         'type': 'mark',
                                         'data': {
                                             'x': 0,
                                             'y': 0,
                                         }
                                     }),
                                     path='/minesweeper/stream/1')
            self.assertEqual(client1.receive()['type'], 'game_change')
