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


class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 15
        self.dx = 8
        self.dy = 8

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), self.radius, "red")

    def update(self):
        self.x += self.dx
        self.y += self.dy

        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.dx = -self.dx
        if self.y <= self.radius or self.y >= HEIGHT - self.radius:
            self.dy = -self.dy

        if self.y + self.radius >= HEIGHT - paddle.height:
            if paddle.x <= self.x <= paddle.x + paddle.width:
                self.dy = -self.dy


paddle = Paddle()
ball = Ball()



def draw():
    screen.fill((255, 155, 0))
    paddle.draw()
    ball.draw()


def update():
    ball.update()

    paddle.on_mouse_move(pg.mouse.get_pos())


pgzrun.go()
