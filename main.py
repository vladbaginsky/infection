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


import math
from random import choice
from random import randint
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
# для графика
import time
# не справился только со временем pygame
import pygame
finished = False
from models import Inf_class, Mob
pygame.init()

from views import WIDTH, HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))

inf = Inf_class(screen, 200)
# создание обьекта инфекции 








# всякие счетчики
counter = 0
time_allinfected = []

inf.options_window(screen)
#вызов меню


clock = pygame.time.Clock()




for i in range(inf.amount):
    a = Mob(screen, randint(0, inf.WIDTH), randint(0, inf.HEIGHT))
    inf.pers.append(a)

#Так же нельзя, чтобы наследовало от объекта, а не от класса? ааааааааааа
# Поэтому будет так:
for per in inf.pers:
    per.rinf = inf.rinf
    per.deathprobability = inf.deathprobability
    per.timetosymptoms = inf.timetosymptoms
    per.timetogetwell = inf.timetogetwell
    per.broun = inf.broun
    per.speed = inf.speed
    
    
inf.pers[0].inf = True

# для графика
start_time = time.time()
time_arr = []
count_arr = []
# задание начального времени по умолчанию у всех
for per in inf.pers:
    per.timeinffirst = start_time

screen.fill(WHITE)
while not finished:
    screen.fill(WHITE)
    
    dt = clock.tick()
    
    for per in inf.pers:
        #print(per.WIDTH)
        per.move(dt)
        per.draw()
        inf.per = per.die(inf.pers)
        per.isolate()
        
        if per.inf == True:
            per.get_well()
        
    
    # count для графика
    counter = 0
    for per in inf.pers:
        if per.inf:
            counter += 1
    
    
    
    count_arr.append(counter)
    time_arr.append(int(time.time()-start_time))
    
    if len(time_allinfected)==0:
        if counter == 0:
            time_allinfected.append(time_arr[-1])
            print(time_allinfected[0])
    
    
    for per1 in inf.pers:
        per1.time = time.time()-per1.timeinffirst
        if per1.inf == True:
            for per2 in inf.pers:
                if per2.inf == True:
                    continue
                if (per1.x-per2.x)**2 + (per1.y-per2.y)**2 < (per1.rinf)**2:
                    per2.inf = not per2.immu
                    per2.timeinffirst = int(time.time())
                        
    
        
                        
    pygame.display.update()
    
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
print(len(inf.pers))
# график

f_interp = interp1d(time_arr , count_arr, bounds_error=False)
x = np.arange(0, int(time.time()-start_time), 1)
#plt.plot(np.array(time_arr), np.array(count_arr) )
plt.plot(x, f_interp(x))
plt.xlabel(r'$time$', fontsize=14)
plt.ylabel(r'$infected$', fontsize=14)
plt.grid(True)
plt.legend(loc='best', fontsize=12)
plt.savefig('figures/figure_with_legend.png')
plt.show()

'''
plt.scatter(np.array(time_arr), np.array(count_arr))
plt.savefig('figures/figure_with_legend.png')
plt.show()
p_f = np.poly1d(np.array(time_arr), np.array(count_arr))
p, v = np.polyfit(time_arr, count_arr, deg=5, cov=True)
plt.plot(arr)
plt.show()
'''


''' plt.plot(np.array([0,100]), p_f(np.array([0,100])))
plt.xlabel(r'$time$', fontsize=14)
plt.ylabel(r'$infected$', fontsize=14)
plt.grid(True)
plt.legend(loc='best', fontsize=12)
plt.savefig('figures/figure_with_legend.png')
plt.show()'''

