import math
from random import choice
from random import randint

import pygame


FPS = 30
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

class Mob:
    def __init__(self, screen: pygame.Surface, x, y, color=BLACK):
        self.x = x
        self.y = y
        self.r = 3
        self.rinf = 5
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.color = BLACK
        self.inf = 0
        self.screen = screen
    
    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
    def move(self, dt):
        self.vx = randint(-10,10)/10
        self.vy = randint(-10,10)/10
        self.x += self.vx * dt
        self.y += self.vy * dt
        #self.vx += self.ax*dt
        
        #self.vy += self.ay*dt
        #if (self.x > WIDTH - 5) or (self.x < 5):
        #    self.vx *= -1
        #if (self.y > HEIGHT - 5) or (self.y < 5):
        #    self.vy *= -1
            
    #def broun_move(self):
        #self.ax = randint(-2, 2)
        #self.ay = randint(-1, 1)

finished = False

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
#screen = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)

clock = pygame.time.Clock()

pers = []

for i in range(100):
    a = Mob(screen, randint(0, WIDTH), randint(0, HEIGHT))
    pers.append(a)

pers[0].color = RED

#screen.fill(WHITE)
while not finished:
    screen.fill(WHITE)
    
    dt = clock.tick()
    
    
    
    
    for per in pers:
        per.move(dt)
        #per.broun_move()
        per.draw()
    
    
    for per1 in pers:
        if per1.color ==RED:
            for per2 in pers:
                if (per1.x-per2.x)**2 + (per1.y-per2.y)**2 < (per1.rinf+per2.rinf)**2:
                    if per1.color == RED or per2.color == RED:
                        per1.color = RED
                        per2.color = RED
        
    pygame.display.update()
    
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
