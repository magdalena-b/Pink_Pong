import pygame, sys
from pygame.locals import *
from random import choice, random


INDIAN_RED = (205, 92, 92)
DARK_SALMON = (233, 150, 122)
DIM_GRAY = (105, 105, 105)
BLACK = (0, 0, 0)

SCREEN_HEIGHT = 300
SCREEN_WIDTH = 400

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0)

PADDLE_HEIGHT = 50
PADDLE_WIDTH = 4

PADDLE_VEL = 7

# enum values
UP = "gora"
DOWN = "dol"

points_r = 0
points_l = 0


class Paddle:
    def __init__(self, x, y, clr, vel):
        self.x = x
        self.y = y
        self.height = PADDLE_HEIGHT
        self.width = PADDLE_WIDTH
        self.color = clr
        self.vel = vel
        
        self.is_moving = False
        self.direction = None


    def draw(self):
        leftx = self.x - self.width/2
        topy = self.y - self.height/2
        coords = pygame.Rect(leftx, topy, self.width, self.height)
        pygame.draw.rect(DISPLAYSURF, self.color, coords, 0)

    def move(self):
        if not self.is_moving:
            return
        
        if self.direction == UP and self.y - self.height/2 > 0:
            self.y -= self.vel 
        elif self.direction == DOWN and self.y + self.height/2 < SCREEN_HEIGHT:
            self.y += self.vel 


class Ball:
    def __init__(self, r, color, vel):
        self.r = r
        self.color = color
        self.vel = vel
        self.reset()


    def draw(self):
        radius = self.r
        pygame.draw.circle(DISPLAYSURF, self.color, (self.x, self.y), self.r)

    def move(self):
        self.x += self.velx
        self.y += self.vely

        if self.y - self.r < 0 or self.y  + self.r > SCREEN_HEIGHT:
            self.vely = - self.vely

        if self.x - self.r < 0:
            if collide(paddle_l, self):
                self.velx = - self.velx
            else:
                self.reset()
                global points_r
                points_r += 1
        elif self.x + self.r > SCREEN_WIDTH:
            if collide(paddle_r, self):
                self.velx = - self.velx
            else:
                self.reset()
                global points_l
                points_l += 1

    def reset(self):
        self.velx = choice(range(self.vel//2, self.vel))
        self.vely = choice(range(self.vel//2, self.vel))

        if random() > 0.5:
            self.velx *= -1
        if random() > 0.5:
            self.vely *= -1

        self.x = SCREEN_WIDTH//2
        self.y = SCREEN_HEIGHT//2


def collide(paddle, ball):
    if abs(ball.y - paddle.y) < paddle.height/2 + ball.r:
        return True
    else:
        return False

def create_points_text():
    text = FONT.render(str(points_l) + " : " + str(points_r), 1, (0,0,0))
    textpos = text.get_rect()
    textpos.centerx = SCREEN_WIDTH/2
    textpos.centery = 15
    return (text, textpos)


pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()
pygame.display.set_caption("Pink Pong IGF 2017")
FONT = pygame.font.Font(None, 30)

paddle_r = Paddle(SCREEN_WIDTH - PADDLE_WIDTH/2, SCREEN_HEIGHT/2, INDIAN_RED, PADDLE_VEL) #right paddle
paddle_l = Paddle(0 + PADDLE_WIDTH/2, SCREEN_HEIGHT/2, DARK_SALMON, PADDLE_VEL) #left paddle
ball = Ball(5, BLACK, 6)

while True: #main loop
    DISPLAYSURF.fill(DIM_GRAY)

    paddle_r.move()
    paddle_l.move()

    paddle_r.draw()
    paddle_l.draw()

    ball.draw()
    ball.move()

    text_to_draw, textpos_to_draw = create_points_text()
    DISPLAYSURF.blit(text_to_draw, textpos_to_draw)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                paddle_r.is_moving = True
                paddle_r.direction = UP
            elif event.key == pygame.K_DOWN:
                paddle_r.is_moving = True
                paddle_r.direction = DOWN
            if event.key == pygame.K_w:
                paddle_l.is_moving = True
                paddle_l.direction = UP
            elif event.key == pygame.K_s:
                paddle_l.is_moving = True
                paddle_l.direction = DOWN

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                paddle_r.is_moving = False
            elif event.key == pygame.K_DOWN:
                paddle_r.is_moving = False
            if event.key == pygame.K_w:
                paddle_l.is_moving = False
            elif event.key == pygame.K_s:
                paddle_l.is_moving = False

        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)