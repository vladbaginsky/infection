import pygame
from random import randint
from views import WIDTH, HEIGHT
from mob_class import Mob
import time

from views import WHITE
from text_class import Text

# если isolation only infected, то изолируем после появления симптомов,
# если no isolation - никого никогда не изолируем,
# если isolation == all - изолируем всех с самого начала
# isolation = "only infected"


class Inf:

    def __init__(self, screen: pygame.Surface, amount=200):
        self.pers = []
        self.time = "не окончена"
        # если isolation only infected, то изолируем после появления симптомов,
        # если no isolation - никого никогда не изолируем,
        # если isolation == all - изолируем всех с самого начала
        self.isolation = "only infected"
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.amount = amount
        self.deathprobability = 15
        # вероятность смерти
        self.screen = screen
        self.rinf = 6
        self.r = 3
        self.timetogetwell = 25
        self.timetosymptoms = 5
        # определяет амплитуду броуновского движения
        self.broun = 10
        # скорость отвечающая за то, как далеко ходят люди, от 0 до 1
        self.speed = 0
        # время до появления симптомов

    def processing(self, dt):
        for per in self.pers:

            per.move(dt)
            per.draw()
            per.die(self.pers, time.time(), self.timetogetwell)
            per.isolate()

            if per.inf:
                per.get_well()
        for per1 in self.pers:
            per1.time = time.time()-per1.timeinffirst
            if per1.inf:
                for per2 in self.pers:
                    if per2.inf:
                        continue
                    a = (per1.x-per2.x)**2
                    b = (per1.y-per2.y)**2
                    c = (self.rinf)**2
                    if a + b < c:
                        per2.inf = not per2.immu
                        per2.timeinffirst = int(time.time())

    def create_mobs(self):
        
        self.pers = []
        print(self.amount)
        for i in range(self.amount):
            a = Mob(self.r, self.screen,
                    randint(0, self.WIDTH), randint(0, self.HEIGHT))
            self.pers.append(a)

        for per in self.pers:
            per.rinf = self.rinf
            per.deathprobability = self.deathprobability
            per.timetosymptoms = self.timetosymptoms
            per.timetogetwell = self.timetogetwell
            per.broun = self.broun
            per.speed = self.speed
            per.isolation = self.isolation

    def options_window(self,):

        self.screen.fill(WHITE)
        stop = 0
        
        t = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        
        t[0] = Text(self.screen, 'label', 'Самоизоляция ', 50, self.isolation)
        t[1] = Text(self.screen, 'label', 'Количество ', 80, self.amount, 10)
        t[2] = Text(self.screen, 
                    'label', 'Радиус инфицирования ', 110, self.rinf, 2)
        t[3] = Text(self.screen, 'label', 'Вероятность смерти ', 140,
                    self.deathprobability, 5)
        t[4] = Text(self.screen, 'label', 'Время до появления ' +
                    'симптомов ', 170, self.timetosymptoms , 5)
        t[5] = Text(self.screen, 'label', 'Время до выздоровления ', 200,
                    self.timetogetwell, 2)
        t[6] = Text(self.screen, 'label', 'Амплитуда Броуновского '+
                  'движения(>0) ', 230, self.broun, 10)
        t[7] = Text(self.screen, 'label', 'Люди ходят в гости/посещают'+
                  ' другие города (0-5)', 260, self.speed, 1)
        t[8] = Text(self.screen, 'but', 'старт ', 400)

        t[8].pos_x = 400
        t[8].r = 70
        while not stop:

            self.screen.fill(WHITE)
    
            t[0].new_text(self.isolation)
            t[1].new_text(self.amount)
            t[2].new_text(self.rinf)
            t[3].new_text(self.deathprobability)
            t[4].new_text(self.timetosymptoms)
            t[5].new_text(self.timetogetwell)
            t[6].new_text(self.broun)
            t[7].new_text(self.speed)

            for element in t:
                element.draw()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if t[0].is_tap(x, y) == "+":
                        if self.isolation == "no":
                            self.isolation = "only infected"
                        elif self.isolation == "only infected":
                            self.isolation = "all"
                        elif self.isolation == "all":
                            self.isolation = "no"
                    if t[0].is_tap(x, y) == "-":
                        if self.isolation == "only infected":
                            self.isolation = "no"
                        elif self.isolation == "no":
                            self.isolation = "all"
                        elif self.isolation == "all":
                            self.isolation = "only infected"
                            
                    self.amount = t[1].tap_processing(x, y) 
                    self.rinf = t[2].tap_processing(x, y) 
                    self.deathprobability = t[3].tap_processing(x, y) 
                    self.timetosymptoms = t[4].tap_processing(x, y) 
                    self.timetogetwell = t[5].tap_processing(x, y) 
                    self.broun = t[6].tap_processing(x, y) 
                    self.speed = t[7].tap_processing(x, y) 
                    
                    stop = t[8].is_tap(x, y)
                        
                    
                if event.type == pygame.QUIT:
                    stop = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        stop = True
            pygame.display.update()

    def set_time_inffirst(self, start_time):
        # задание начального времени по умолчанию у всех
        for per in self.pers:
            per.timeinffirst = start_time

    def finish_window(self, screen):
        
        screen.fill(WHITE)
        stop = 0
        
        t= [0, 1, 2, 3, 4, 5, 6]
        
        t[0] = Text(self.screen, 'but', 'Население ' + str(self.amount), 20)
        t[1] = Text(self.screen, 'but', 'Количество выживших ' +
                    str(len(self.pers)), 50)
        t[2] = Text(self.screen, 
                    'but', 'Длительность эпидемии: ' + str(self.time),  80)
        
        t[3] = Text(self.screen, 'but', 'График сохранен figures/figure.png',
                    170)
        t[4] = Text(self.screen, 'but', 'Завершить ', 400)
        t[5] = Text(self.screen, 'but', 'Заново ', 400)
        t[4].r = 75
        t[5].r = 75
        t[4].pos_x = 310
        t[5].pos_x = 470
        t[6] = Text(self.screen, 'but', 'Вирус убил первого своего'+
                    ' носителя,', 110)
        
        while not stop:

            screen.fill(WHITE)
            for element in t:
                if element != t[6]:  
                    element.draw()
            if self.time == 0:
                t[6].draw()   
            
            

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if t[5].is_tap(x, y):
                        stop = True
                        return False
                    if t[4].is_tap(x,y):
                        stop = True
                        return True
                if event.type == pygame.QUIT:
                    stop = True
                    return True
