import pytest
import numpy as np
from snake_game import *


def test_start():
    assert len(game.snake) == 6
    assert game.food < (23, 20)
    assert game.playing_box['Height'] == 23
    assert game.playing_box['Width']  == 20


def test_init():
    for object_ in game.objects:
        assert game.objects[object_].shape == (24, 24, 4)


def test_set_direction_and_move():
    game.set_direction('U')
    assert game.snake[0][-1] == 'U'
    game.move()
    assert game.snake[1][-1] == 'U'
    assert game.snake[2][-1] != 'U'
    game.set_direction('D')
    assert game.snake[0][-1] != 'D'
    game.set_direction('L')
    for part in game.snake:
        assert part[-1] == 'L'
        game.move()


def test_grow():
    game.set_direction('R')
    game.grow()
    assert len(game.snake) == 7 and int(game.snake[-1][1]) == int(game.snake[-2][1]) + 1
    game.set_direction('D')
    for i in range(len(game.snake)):
        game.move()
    game.grow()
    assert len(game.snake) == 8 and int(game.snake[-1][0]) == int(game.snake[-2][0]) + 1


def test_get_data():
    npdata = game.get_np_data()
    assert npdata.shape == (576, 480, 4)


def test_spawn_food():
    for i in range(1000):
        game.spawn_food()
        assert game.food not in [(int(x), int(y)) for x, y, d in game.snake]


def test_update_move_restart():
    game.game_over = False
    game.update(1/10)
    assert game.time == 1/10
    assert len(game.snake) == 8
    game.score = 454
    game.update(1/10)
    assert game.you_won is True
    game.restart()
    assert not game.you_won
    assert game.high_score == 454
    assert game.score == 0

