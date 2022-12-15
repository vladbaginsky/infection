import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
# для графика
import time
# не справился только со временем pygame
import pygame

from game_class import Inf

from views import WIDTH, HEIGHT

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


screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.init()

end = False
while not end:

    inf = Inf(screen, 200)
    # создание обьекта инфекции

    # всякие счетчики
    counter = 0
    time_allinfected = []

    inf.options_window()
    # вызов меню

    clock = pygame.time.Clock()

    inf.create_mobs()
    # создание людей

    inf.pers[0].inf = True

    # для графика
    start_time = time.time()
    time_arr = []
    count_arr = []

    inf.set_time_inffirst(start_time)

    screen.fill(WHITE)
    finished = False
    while not finished:
        screen.fill(WHITE)

        dt = clock.tick()

        inf.processing(dt)
        # обработка движения, смерти и выздоравления. Обработка заражения

        inf.button('Прервать ',
                   4, (180, 0, 0), (400, 500))

        # count для графика
        counter = 0
        for per in inf.pers:
            if per.inf:
                counter += 1

        count_arr.append(counter)
        time_arr.append(int(time.time()-start_time))

        if len(time_allinfected) == 0:
            if counter == 0:

                time_allinfected.append(time_arr[-1])
                inf.time = time_arr[-1]
                print(time_allinfected[0])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (x-400)**2 + (y-500)**2 < 75**2:
                    finished = True
            if event.type == pygame.QUIT:
                finished = True
                end = True

    end = inf.finish_window(screen)

    # график
    f_interp = interp1d(time_arr, count_arr, bounds_error=False)
    x = np.arange(0, int(time.time()-start_time), 1)
    # plt.plot(np.array(time_arr), np.array(count_arr) )
    plt.plot(x, f_interp(x))
    plt.xlabel(r'$time$', fontsize=14)
    plt.ylabel(r'$infected$', fontsize=14)
    plt.grid(True)
    plt.legend(loc='best', fontsize=12)
    plt.savefig('figures/figure.png')
pygame.quit()
