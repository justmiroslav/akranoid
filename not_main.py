import pgzrun
import pygame as pg
import time

WIDTH = 800
HEIGHT = 600
lives = 3
heart_image = pg.image.load("heart.png")
heart = pg.transform.scale(heart_image, (40, 40))
heart_x = WIDTH // 2
heart_y = 0
heart_dy = 1
heart_timer = 0
bonus_x = WIDTH - 20
bonus_y = 0
bonus_dy = 3
bonus_timer = 0
bonus_start = 0
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
    def __init__(self, x, y, strength):
        self.x = x
        self.y = y
        self.width = 110
        self.height = 30
        self.strength = strength
        self.active = True

    def draw(self):
        if self.active:
            if self.strength == 1:
                color = "blue"
            elif self.strength == 2:
                color = "green"
            else:
                color = "purple"
            screen.draw.filled_rect(Rect((self.x, self.y), (self.width, self.height)), color)

    def collision(self, ball):
        if self.active:
            if ball.x + ball.radius > self.x and ball.x - ball.radius < self.x + self.width:
                if ball.y + ball.radius > self.y and ball.y - ball.radius < self.y + self.height:
                    self.strength -= 1
                    if self.strength == 0:
                        self.active = False
                    if ball.x + ball.radius >= self.x + self.width or ball.x - ball.radius <= self.x:
                        ball.dx = -ball.dx
                    if ball.y + ball.radius >= self.y + self.height or ball.y - ball.radius <= self.y:
                        ball.dy = -ball.dy


paddle = Paddle()
ball = Ball()
obstacles = []
for i in range(6):
    for j in range(4):
        if i in [0, 5]:
            strength = 1
        elif i in [1, 4]:
            strength = 2
        else:
            strength = 3
        obstacles.append(Obstacle(30 + i * 125, 75 + j * 50, strength))


def draw():
    global game_win, heart_x, heart_y, lives, bonus_x, bonus_y
    screen.clear()
    screen.fill((255, 155, 0))
    paddle.draw()
    ball.draw()
    for obstacle in obstacles:
        obstacle.draw()
    if not game_over:
        if pg.time.get_ticks() >= 10000:
            if pg.time.get_ticks() >= 25000:
                screen.draw.filled_circle((bonus_x, bonus_y), 20, "white")
            screen.blit(heart, (heart_x, heart_y))
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
            global heart_timer, heart_x, heart_y, heart_dy, lives, bonus_x, bonus_y, bonus_dy, bonus_timer, bonus_start
            ball.update()
            paddle.on_mouse_move(pg.mouse.get_pos())
            timer = pg.time.get_ticks()
            if timer - heart_timer >= 10000:
                if timer - bonus_timer >= 25000:
                    bonus_x = WIDTH - 20
                    bonus_y = 0
                    bonus_timer = timer
                heart_x = WIDTH // 2
                heart_y = 0
                heart_timer = timer
            heart_y += heart_dy
            bonus_y += bonus_dy
            add_platform = pg.Rect(paddle.x, paddle.y, paddle.width, paddle.height)
            add_bonus = pg.Rect(bonus_x, bonus_y, 20, 20)
            if heart_y + 20 >= HEIGHT - paddle.height:
                if paddle.x <= heart_x <= paddle.x + paddle.width:
                    lives += 1
                    heart_y = -heart_y
            if add_bonus.colliderect(add_platform):
                paddle.width *= 1.5
                bonus_y = -bonus_y
                bonus_start = timer
            if pg.time.get_ticks() - bonus_start >= 3000:
                paddle.width = 150
                bonus_start = 0
        else:
            time.sleep(1.2)
            pg.quit()
    else:
        time.sleep(1.2)
        pg.quit()


pgzrun.go()
