import pgzrun
import pygame as pg
import time

WIDTH = 800
HEIGHT = 600
lives = 3
game_over = False
game_win = False


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
        self.dx = 2
        self.dy = 2

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

        if self.y >= HEIGHT - paddle.height and (self.x < paddle.x or self.x > paddle.x + paddle.width):
            global lives
            lives -= 1
            if lives > 0:
                if lives // 2:
                    self.x = WIDTH // 2
                    self.y = HEIGHT // 2
                    self.dx = -8
                    self.dy = 8
                else:
                    self.x = WIDTH // 2
                    self.y = HEIGHT // 2
                    self.dx = 8
                    self.dy = 8
            else:
                global game_over
                game_over = True
        for obstacle in obstacles:
            obstacle.collision(self)


class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.active = True

    def draw(self):
        if self.active:
            screen.draw.filled_circle((self.x, self.y), self.radius, "blue")

    def collision(self, ball):
        if self.active:
            if (ball.x - self.x)**2 + (ball.y - self.y)**2 <= self.radius**2:
                ball.dy = -ball.dy
                self.active = False


paddle = Paddle()
ball = Ball()
heart_image = pg.image.load("heart.png")
heart = pg.transform.scale(heart_image, (40, 40))
obstacles = []
for i in range(16):
    for j in range(4):
        obstacles.append(Obstacle(25 + i * 50, 75 + j * 50))


def draw():
    global game_win
    screen.fill((255, 155, 0))
    paddle.draw()
    ball.draw()
    for obstacle in obstacles:
        obstacle.draw()
    if not game_over:
        for p in range(lives):
            screen.blit(heart, (4 + p * 50, 10))
        if not any(obstacle.active for obstacle in obstacles):
            game_win = True
            screen.draw.text("YOU WON!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="black")
    if game_over:
        screen.draw.text("GAME OVER!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="black")


def update():
    if not game_over:
        if not game_win:
            ball.update()
            paddle.on_mouse_move(pg.mouse.get_pos())
        else:
            time.sleep(1.2)
            pg.quit()
    else:
        time.sleep(1.2)
        pg.quit()


pgzrun.go()
