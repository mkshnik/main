import pyglet
import numpy as np
from pyglet.window import key
from pyglet.gl import *
from random import randint, randrange
# from pyglet.window import FPSDisplay


class CGame:
    """
    Class provides all operations for snake game and does
    all automatically once the game is started

    Attributes:
        -> playing_box(dict[str:int]): stores 'Width' and 'Height' of playing area
        -> objects (dict[str:numpy.array]): stores all game objects
        -> food (tuple): coordinates of the food
        -> step (int): size of step for each moving object per frame
        -> game_over (boolean): loosed game indicator (True is the game is lost)
        -> you_won (boolean): won game indicator (True if game is won)
        -> win_score (int): score required to win the game
        -> score (int): stores score of current game
        -> time (int): stores time of current game
        -> high_score (int): highest earned score during current reboot
        -> window (pyglet.window): game window
        -> field_image (pyglet.ImageData): stores background image
        -> background (pyglet.Sprite): stores background sprite from field_image
        -> snake (numpy.array): stores coordinates and directions of each park of snake
    """

    def __init__(self):
        """
        Constructor for CGame class.
        """
        self.playing_box = {'Width': 20, 'Height': 23}
        self.init_parts()
        self.food       = tuple()
        self.step       = 24
        self.game_over  = False
        self.you_won    = False
        self.win_score  = 454
        self.score      = 0
        self.high_score = 0
        self.time       = 0

    def init_parts(self):
        """
        Method initializes and fills with pixel data all game objects
        and then initializes attribute 'objects'
        """
        t_food = np.full((24, 24, 4), [171, 141, 59, 255])
        t_space = np.full((24, 24, 4), 255)
        t_body = t_space.copy()
        t_head = t_body.copy()
        t_body[1:-1, 1:-1, :] = [255, 105, 180, 255]
        t_head[1:-1, 1:-1, :] = [0, 206, 209, 255]
        t_food[1:-1, 1:-1, :] = [255, 127, 80, 255]
        self.objects = {'BODY': t_body, 'HEAD': t_head, 'FOOD': t_food, 'SPACE': t_space}

    def update_score(self):
        """
        Method initializes and returns label to show current, high scores and the time on the screen
        """
        out_score = pyglet.text.Label('Score: {}                '
                                      'High: {}                              '
                                      'Time: {}'
                                      .format(self.score, self.high_score, int(self.time)),
                                      font_name='Default',
                                      font_size=13,
                                      x=5, y=559,
                                      color=(0, 0, 0, 255))
        return out_score

    def open_window(self):
        """
        Method initializes 'window' attribute with as pyglet.window
        """
        w, h = int(self.background.width), int(self.background.height)
        self.window = pyglet.window.Window(w, h, caption='Змiя', resizable=False)
        ###
        # wx, wy = self.window.get_location()
        # self.fps_display = FPSDisplay(self.window)
        # self.window.set_location(wx + 1300, wy + 100)
        ###

    def set_background(self):
        """
        Method initializes attribute 'field_image'
        """
        self.field_image = pyglet.image.load('background.png')
        self.background = pyglet.sprite.Sprite(self.field_image, x=0, y=0, subpixel=True)
        self.background.update(scale_x=1, scale_y=1)

    def set_direction(self, direction):
        """
        Method sets new direction to the snake if its not an opposite to a current one
        :param direction: Direction to be set
        """
        oposites = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}
        if oposites[direction] != self.snake[0][-1]:
            self.snake[0][-1] = direction

    def grow(self):
        """
        Method adds new part of snake to it's end with coordinates and direction depends
        """
        x, y, direction = self.snake[-1]
        y = int(y)
        x = int(x)
        if direction == 'R':
            self.snake = np.append(self.snake, [(x, y - 1, direction)], axis=0)
        elif direction == 'L':
            self.snake = np.append(self.snake, [(x, y + 1, str(direction))], axis=0)
        elif direction == 'U':
            self.snake = np.append(self.snake, [(x - 1, y, str(direction))], axis=0)
        elif direction == 'D':
            self.snake = np.append(self.snake, [(x + 1, y, str(direction))], axis=0)

    def printer(self, coords, obj):
        x, ex = (int(coords[0]) - 1) * self.step + self.step, int(coords[0]) * self.step + self.step
        y, ey = (int(coords[1]) - 1) * self.step + self.step, int(coords[1]) * self.step + self.step
        x = int(x)
        ex = int(ex)
        y = int(y)
        ey = int(ey)
        npdata = self.get_np_data()
        npdata[x:ex, y:ey, :] = obj
        self.set_np_data(npdata)

    def spawn_food(self):
        self.food = (randrange(0, self.playing_box['Height'] - 1),
                     randrange(1, self.playing_box['Width']) - 1)
        if self.food in [(int(x), int(y)) for (x, y, d) in self.snake]:
            self.spawn_food()
        else:
            self.printer((self.food[0], self.food[1]), self.objects['FOOD'])

    def start(self):
        self.snake = np.array([
            (0, 5, 'R'),
            (0, 4, 'R'),
            (0, 3, 'R'),
            (0, 2, 'R'),
            (0, 1, 'R'),
            (0, 0, 'R')
        ])
        self.spawn_food()

    def get_np_data(self):
        self.image_data = self.field_image.get_image_data()
        data = self.image_data.get_data('RGBA', 4 * self.image_data.width)
        npdata = np.array(np.frombuffer(data, dtype=np.uint8))
        npdata = np.reshape(npdata, (576, 480, 4))
        return npdata

    def set_np_data(self, npdata):
        npdata = np.clip(npdata, 0, 255)
        bytedata = npdata.tobytes()
        self.image_data.set_data('RGBA', 4 * self.image_data.width, bytedata)
        self.field_image = self.image_data
        self.background = pyglet.sprite.Sprite(self.field_image, x=0, y=0, subpixel=False)
        self.background.update(scale_x=1, scale_y=1)

    def go_to_direction(self, i):
        x, y, direction = self.snake[i]
        x = int(x)
        y = int(y)
        if y == self.playing_box['Width'] - 1 and direction == 'R':
            y = -1

        if y == 0 and direction == 'L':
            y = self.playing_box['Width']

        if x == self.playing_box['Height'] - 1 and direction == 'U':
            x = -1

        if x == 0 and direction == 'D':
            x = self.playing_box['Height']

        if direction == 'R':
            self.snake[i][:2] = [x, y + 1]
        if direction == 'L':
            self.snake[i][:2] = [x, y - 1]
        if direction == 'U':
            self.snake[i][:2] = [x + 1, y]
        if direction == 'D':
            self.snake[i][:2] = [x - 1, y]

    def move(self):
        x, y, tmp_direction = self.snake[0]
        if int(x) == self.food[0] and int(y) == self.food[1]:
            self.grow()
            self.score += 1
            self.spawn_food()
        self.go_to_direction(0)
        x, y = self.snake[0][:2]
        if (x, y) in [(x, y) for x, y, d in self.snake[1:-1]]:
            self.game_over = True
        for i in range(1, len(self.snake)):
            self.go_to_direction(i)
            old_direction = self.snake[i][2]
            self.snake[i][2] = tmp_direction
            tmp_direction = old_direction

    def draw(self):
        self.printer(self.snake[-1][:2], self.objects['SPACE'])
        for i in range(1, len(self.snake) - 1):
            self.printer(self.snake[i][:2], self.objects['BODY'])
        self.printer(self.snake[0][:2], self.objects['HEAD'])

    def restart(self):
        self.game_over = False
        self.you_won = False
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.time = 0
        self.set_background()
        self.start()

    def update(self, dt):
        if not self.game_over and not self.you_won:
            self.move()
            self.draw()
            self.time += dt
            if self.score == self.win_score:
                self.you_won = True
        self.out_score = self.update_score()


game = CGame()
game.set_background()
game.update_score()
game.open_window()
game.out_score = game.update_score()
game.start()


restart_sign = pyglet.text.Label("press 'Space' to restart",
                                 font_name='Default',
                                 font_size=10,
                                 x=game.window.width // 2 - 5,
                                 y=game.window.height // 2 - 20,
                                 anchor_x='center', anchor_y='center')

gameover_sign = pyglet.image.load('gameover.png')
gameover_sprite = pyglet.sprite.Sprite(gameover_sign, x=90, y=252, subpixel=True)
gameover_sprite.update(scale_x=1, scale_y=1)

won_sign = pyglet.image.load('win.jpeg')
won_sprite = pyglet.sprite.Sprite(won_sign, x=80, y=252, subpixel=True)
won_sprite.update(scale_x=1, scale_y=1)


@game.window.event
def on_draw():
    game.window.clear()
    game.background.draw()
    # game.fps_display.draw()
    game.out_score.draw()
    if game.game_over:
        gameover_sprite.draw()
        restart_sign.draw()
    if game.you_won:
        won_sprite.draw()
        restart_sign.draw()


@game.window.event
def on_key_press(symbol, modifiers):
    keys = {key.UP: 'U', key.DOWN: 'D', key.LEFT: 'L', key.RIGHT: 'R'}
    if symbol in keys:
        game.set_direction(keys[symbol])
    if symbol == key.SPACE and (game.game_over or game.you_won):
        game.restart()


if __name__ == '__main__':
    pyglet.clock.schedule_interval(game.update, 1/10)
    pyglet.app.run()
