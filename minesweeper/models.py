from django.db import models
import json
import numpy as np
import itertools


class GameData(models.Model):

    data = models.TextField()


class Game():
    """The game object."""

    game_map = None
    # game_mask is an array with the same shape as game_map, visible: 1, marked mines: -1
    game_mask = None

    def new(self, w, h, mines_total):
        non_mines_count = max(w * h - mines_total, 0)
        mines_count = min(w * h, mines_total)
        tmp_map = np.full(non_mines_count, 0)
        tmp_map = np.append(tmp_map, np.full(mines_count, -1))
        np.random.shuffle(tmp_map)
        self.game_map = np.reshape(tmp_map, (h, w))
        self.game_mask = np.full(self.game_map.shape, 0)
        self.flush()

    def flush(self):
        """Flush numbers around mines"""

        # Change surrounding tiles around mines, it may be optmized in the futre Notice that x y is reversing h w
        (h, w) = self.game_map.shape
        for (x, y), value in np.ndenumerate(self.game_map):
            if value == -1:
                for i, j in itertools.product([x-1, x, x+1], [y-1, y, y + 1]):
                    if (0 <= i < h) and (0 <= j < w) and self.game_map[i, j] != -1:
                        self.game_map[i, j] += 1

    def mark(self, x, y):
        if self.get_user_map()[x, y] > 0:
            return
        elif self.get_user_map()[x, y] == -1:
            self.game_mask[x, y] = 0
        else:
            self.game_mask[x, y] = -1

    def reveal(self, x, y):
        """Reveal the clicked tile"""

        (h, w) = self.game_map.shape
        if self.game_mask[x, y] != 0:
            return True
        elif self.game_map[x, y] < 0:
            return False
        elif self.game_map[x, y] > 0:
            self.game_mask[x, y] = 1
        else:
            self.game_mask[x, y] = 1
            for i, j in itertools.product([x-1, x, x+1], [y-1, y, y + 1]):
                if (0 <= i < h) and (0 <= j < w) and self.game_map[i, j] != -1:
                    self.reveal(i, j)

    def get_user_map(self):
        """Merge game_map with game_mask."""

        user_map = np.full(self.game_mask.shape, 0)
        for (x, y), value in np.ndenumerate(self.game_map):
            if (self.game_mask[x, y] > 0):
                user_map[x, y] = self.game_map[x, y]
            elif (self.game_mask[x, y] == -1):
                user_map[x, y] = -1
            else:
                user_map[x, y] = -2

        return user_map

    def load(self, game_id):
        self.game_id = game_id
        game_data, created = GameData.objects.get_or_create(pk=game_id)
        if created:
            self.new(5, 5, 5)
        else:
            try:
                data = json.loads(game_data.data)
                self.game_map = np.array(data['game_map'])
                self.game_mask = np.array(data['game_mask'])
            except:
                self.new(5, 5, 5)

    def save(self, **kwargs):
        game_data, created = GameData.objects.get_or_create(pk=self.game_id)
        game_data.data = json.dumps({
            'game_map': self.game_map.tolist(),
            'game_mask': self.game_mask.tolist(),
        })
        game_data.save()
