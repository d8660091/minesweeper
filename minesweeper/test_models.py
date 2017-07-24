from django.test import TestCase

import numpy as np
from .models import Game


class GameTests(TestCase):

    def test_game_can_construct_map_by_parameters(self):
        game = Game()
        game.new(4, 5, 5)
        self.assertEqual(game.game_map.shape, (5, 4))
        self.assertEqual(game.game_mask.shape, (5, 4))
        self.assertEqual(game.game_mask[0, 0], 0)

    def test_game_can_handle_too_big_mines_total(self):
        game = Game()
        game.new(3, 5, 99)
        self.assertEqual(game.game_map.shape, (5, 3))

    def test_game_can_flush_map_correctly(self):
        game = Game()
        game.game_map = np.array([[0, 0], [0, -1]])
        game.flush()
        self.assertTrue(
            np.array_equal(game.game_map,
                           np.array([[1, 1], [1, -1]]))
        )

    def test_game_can_flush_map_correctly_2(self):
        game = Game()
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
        game = Game()
        game.new(3, 3, 1)
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
        game = Game()
        game.new(3, 3, 1)
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
        game = Game()
        game.new(3, 3, 1)
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
        game = Game()
        game.new(3, 3, 1)
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

    def test_game_reveal_return_false(self):
        game = Game()
        game.new(3, 3, 1)
        game.game_map = np.array([[-1, 0, 0],
                                  [0, -1, 0],
                                  [0, 0, 0]])
        game.flush()
        game.reveal(0, 0)
        self.assertFalse(game.reveal(0, 0))

    def test_game_mark_mine(self):
        game = Game()
        game.new(3, 3, 1)
        game.game_map = np.array([[-1, 0, 0],
                                  [0, -1, 0],
                                  [0, 0, 0]])
        game.flush()
        game.mark(0, 0)
        self.assertEqual(game.game_mask[0, 0], -1)

    def test_game_reveal_does_not_overide_user_marks(self):
        game = Game()
        game.new(3, 3, 1)
        game.game_map = np.array([[0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, -1]])
        game.flush()
        game.game_mask[1, 0] = -1
        game.reveal(0, 0)
        self.assertTrue(
            np.array_equal(game.get_user_map(),
                           np.array([[0, 0, 0],
                                     [-1, 1, 1],
                                     [-2, -2, -2]]))
        )

    def test_game_does_not_mark_digits(self):
        game = Game()
        game.new(3, 3, 1)
        game.game_map = np.array([[0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, -1]])
        game.flush()
        game.game_mask[1, 1] = 1
        game.mark(1, 1)
        self.assertEqual(game.get_user_map()[1, 1], 1)

    def test_game_can_end_by_mistake(self):
        game = Game()
        game.new(3, 3, 1)
        game.game_map = np.array([[0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, -1]])
        game.flush()
        game.game_mask[1, 1] = 1
        game.reveal(2, 2)
        self.assertEqual(game.game_ended, True)
        self.assertEqual(game.game_mask[2, 2], -2)

    def test_game_is_not_ended_after_calling_new(self):
        game = Game()
        game.game_ended = True
        game.new(3, 3, 1)
        self.assertEqual(game.game_ended, False)

    def test_user_map_is_rendered_after_game_end(self):
        game = Game()
        game.game_ended = True
        game.game_map = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, -1, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, -1, 0, 0]])
        game.flush()
        game.game_mask = np.array([[1, 1, 1, -1, 0, 0, 0, 0],
                                  [1, 1, 1, -2, 0, 0, 0, 0],
                                  [1, 1, 1, 1, 0, 0, 0, 0]])
        game.game_ended = True
        self.assertTrue(
            np.array_equal(game.get_user_map(),
                           np.array([[0, 0, 1, -4, -2, -2, -2, -2],
                                     [0, 0, 1, -5, -2, -2, -2, -2],
                                     [0, 0, 1, 1, -2, -3, -2, -2]]))
        )

    def test_reveal_does_not_work_if_game_is_ended(self):
        game = Game()
        game.new(3, 3, 1)
        game.game_map = np.array([[0, 0, 0],
                                  [0, 0, 0],
                                  [0, 0, -1]])
        game.flush()
        game.game_ended = True
        self.assertEqual(game.game_mask[0, 0], 0)
        game.reveal(0, 0)
        self.assertEqual(game.game_mask[0, 0], 0)

    def test_unmark_mine(self):
        game = Game()
        game.new(3, 3, 1)
        game.game_mask[0, 0] = -1
        game.mark(0, 0)
        self.assertEqual(game.game_mask[0, 0], 0)

    def test_do_not_mark_after_game_end(self):
        game = Game()
        game.new(3, 3, 1)
        game.game_mask[0, 0] = 0
        game.game_ended = True
        game.mark(0, 0)
        self.assertNotEqual(game.game_mask[0, 0], -1)

    def test_do_not_mark_for_zer_tile(self):
        game = Game()
        game.new(3, 3, 1)
        game.game_mask[0, 0] = 1
        game.game_map[0, 0] = 0
        game.mark(0, 0)
        self.assertNotEqual(game.game_mask[0, 0], -1)

    def test_do_oversize(self):
        game = Game()
        game.new(61, 61, 1)
        self.assertEqual(game.game_map.shape, (60, 60))
