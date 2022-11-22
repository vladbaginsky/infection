import math
from random import choice
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import time
# не справился только со временем pygame

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

WIDTH = 500
HEIGHT = 400


class Mob:
    def __init__(self, screen: pygame.Surface, x, y, color=BLACK, probab = 0.1):
        self.x = x
        self.y = y
        self.r = 3
        self.rinf = 6
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.color = BLACK
        self.inf = False
        self.screen = screen
        self.probab = probab        
        self.immu = False
        
    
        
    def draw(self):
        if self.inf:
            
            self.color = RED
            pygame.draw.circle(self.screen, RED, 
                               (self.x, self.y), self.rinf, 1)
        
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
        if (self.x > WIDTH - 5):
            self.x = WIDTH - 5
        if (self.x < 5):
            self.x =  5
        if (self.y > HEIGHT - 5):
            self.y = HEIGHT - 5
        if (self.y <  5):
            self.y =  5
            
    #def broun_move(self):
        #self.ax = randint(-2, 2)
        #self.ay = randint(-1, 1)

finished = False

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
#screen = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)

clock = pygame.time.Clock()

# для графика
start_time = time.time()
time_arr = []
count_arr = []

pers = []

for i in range(100):
    a = Mob(screen, randint(0, WIDTH), randint(0, HEIGHT))
    pers.append(a)

pers[0].inf = True

counter = 0

screen.fill(WHITE)
while not finished:
    screen.fill(WHITE)
    
    dt = clock.tick()
    
    for per in pers:
        
        per.move(dt)
        per.draw()
    
    # count для графика
    counter = 0
    for per in pers:
        if per.inf:
            counter += 1
            
    count_arr.append(counter)
    time_arr.append(int(time.time()-start_time))
    
    
    
    for per1 in pers:
        if per1.inf == True:
            for per2 in pers:
                
                if (per1.x-per2.x)**2 + (per1.y-per2.y)**2 < (per1.rinf)**2:
                    N = randint(0, 10000)
                    # Обработка заражения с определенной вероятностью
                    if N<= per2.probab*10000:
                        per2.inf = True
                        
                        
    pygame.display.update()
    
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
plt.plot(time_arr, count_arr)
plt.show()