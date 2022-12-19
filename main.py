import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
# для графика
import time
# не справился только со временем pygame
import pygame

from game_class import Inf
from text_class import Text
from views import WIDTH, HEIGHT, WHITE




screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.init()


inf = Inf(screen, 200)
# создание обьекта инфекции

stop_lable = Text(inf.screen,"but", "Прервать", 400)
stop_lable.pos_x = 400
stop_lable.r = 80

end = False
while not end:
    
    
    # всякие счетчики
    counter = 0
    time_allinfected = []
    inf.options_window()
    # вызов меню
    # print(str(inf.amount) + 'sd')
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

        stop_lable.draw()

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
                #print(time_allinfected[0])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if stop_lable.tap_processing(x, y):
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
