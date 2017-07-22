from django.test import TestCase

import numpy as np
from .consumers import Game


class GameTests(TestCase):

    def test_game_can_construct_map_by_parameters(self):
        game = Game(4, 5, 5)
        self.assertEqual(game.game_map.shape, (5, 4))
        self.assertEqual(game.game_mask.shape, (5, 4))
        self.assertEqual(game.game_mask[0, 0], 0)

    def test_game_can_handle_too_big_mines_total(self):
        game = Game(3, 5, 99)
        self.assertEqual(game.game_map.shape, (5, 3))

    def test_game_can_flush_map_correctly(self):
        game = Game(5, 5, 1)
        game.game_map = np.array([[0, 0], [0, -1]])
        game.flush()
        self.assertTrue(
            np.array_equal(game.game_map,
                           np.array([[1, 1], [1, -1]]))
        )

    def test_game_can_flush_map_correctly_2(self):
        game = Game(5, 5, 1)
        game.game_map = np.array([[0, -1, 0],
                                  [0, 0, -1],
                                  [0, -1, 0]])
        game.flush()
        self.assertTrue(
            np.array_equal(game.game_map,
                           np.array([[1, -1, 2],
                                     [2, 3, -1],
                                     [1, -1, 2]]))
        )

    def test_game_reveal_a_tile(self):
        game = Game(3, 3, 0)
        game.game_map = np.array([[0, 0, -1],
                                  [0, 0, 0],
                                  [0, 0, -1]])
        game.flush()
        game.reveal(0, 0)
        self.assertTrue(
            np.array_equal(game.game_mask,
                           np.array([[1, 1, 0],
                                     [1, 1, 0],
                                     [1, 1, 0]]))
        )

    def test_game_reveal_a_tile_2(self):
        game = Game(3, 3, 0)
        game.game_map = np.array([[0, 0, 0],
                                  [0, -1, 0],
                                  [0, 0, 0]])
        game.flush()
        game.reveal(0, 0)
        self.assertTrue(
            np.array_equal(game.game_mask,
                           np.array([[1, 0, 0],
                                     [0, 0, 0],
                                     [0, 0, 0]]))
        )

    def test_game_return_user_map(self):
        game = Game(3, 3, 0)
        game.game_map = np.array([[0, 0, 0],
                                  [0, -1, 0],
                                  [0, 0, 0]])
        game.flush()
        self.assertTrue(
            np.array_equal(game.get_user_map(),
                           np.array([[-2, -2, -2],
                                     [-2, -2, -2],
                                     [-2, -2, -2]]))
        )

    def test_game_return_user_map_2(self):
        game = Game(3, 3, 0)
        game.game_map = np.array([[0, 0, 0],
                                  [0, -1, 0],
                                  [0, 0, 0]])
        game.flush()
        game.reveal(0, 0)
        self.assertTrue(
            np.array_equal(game.get_user_map(),
                           np.array([[1, -2, -2],
                                     [-2, -2, -2],
                                     [-2, -2, -2]]))
        )
