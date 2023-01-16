import pgzrun
import pygame as pg

WIDTH = 800
HEIGHT = 600


class Paddle:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 20
        self.width = 150
        self.height = 30

    def draw(self):
        screen.draw.filled_rect(Rect((self.x, self.y), (self.width, self.height)), "black")

    def on_mouse_move(self, pos):
        self.x = pos[0]
        self.x = max(0, self.x)
        self.x = min(WIDTH - self.width, self.x)


paddle = Paddle()


def draw():
    screen.fill((255, 155, 0))
    paddle.draw()


def update():
    paddle.on_mouse_move(pg.mouse.get_pos())


pgzrun.go()
