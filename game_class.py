import pygame
from random import randint
from views import WIDTH, HEIGHT
from mob_class import Mob
import time


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
        self.rinf = 16
        self.r = 3
        self.timetogetwell = 25
        self.timetosymptoms = 5
        # определяет амплитуду броуновского движения
        self.broun = 10
        # скорость отвечающая за то, как далеко ходят люди, от 0 до 1
        self.speed = 0.5
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

    def button(self, text, num, col, pos):
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render(text, num, (180, 0, 0))
        self.screen.blit(text1, pos)

    def button_plus(self,  pos):
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render("+", 4, (180, 0, 0))
        self.screen.blit(text1, pos)

    def button_minus(self,  pos):
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render("-", 4, (180, 0, 0))
        self.screen.blit(text1, pos)

    def options_window(self,):

        self.screen.fill(WHITE)
        stop = 0

        while not stop:
            self.screen.fill(WHITE)

            self.button('Самоизоляция ' + str(self.isolation),
                        4, (180, 0, 0), (10, 50))
            self.button('Количество ' + str(self.amount), 4,
                        (180, 0, 0), (10, 80))
            self.button('Радиус инфицирования ' + str(self.rinf), 4,
                        (180, 0, 0), (10, 110))
            self.button('Вероятность смерти ' +
                        str(self.deathprobability), 4, (180, 0, 0), (10, 140))
            self.button('Время до появления ' +
                        'симптомов ' + str(self.timetosymptoms),
                        4, (180, 0, 0), (10, 170))
            self.button('Время до выздоровления ' +
                        str(self.timetogetwell), 4, (180, 0, 0), (10, 200))
            self.button('Амплитуда Броуновского движения(>0) ' +
                        str(self.broun), 4, (180, 0, 0), (10, 230))
            self.button('Люди ходят в' +
                         ' гости/посещают другие города (0-2)' +
                         str(self.speed), 4, (180, 0, 0), (10, 260))

            self.button_plus((800, 50))
            self.button_minus((770, 50))

            self.button_plus((800, 80))
            self.button_minus((770, 80))

            self.button_plus((800, 110))
            self.button_minus((770, 110))

            self.button_plus((800, 140))
            self.button_minus((770, 140))

            self.button_plus((800, 170))
            self.button_minus((770, 170))

            self.button_plus((800, 200))
            self.button_minus((770, 200))

            self.button_plus((800, 230))
            self.button_minus((770, 230))

            self.button_plus((800, 260))
            self.button_minus((770, 260))

            self.button('старт ', 4, (180, 0, 0), (400, 400))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    if (x-800)**2 + (y-50)**2 < 15**2:

                        if self.isolation == "no":
                            self.isolation = "only infected"
                        elif self.isolation == "only infected":
                            self.isolation = "all"
                        elif self.isolation == "all":
                            self.isolation = "no"

                    if (x-770)**2 + (y-50)**2 < 15**2:
                        if self.isolation == "only infected":
                            self.isolation = "no"
                        elif self.isolation == "no":
                            self.isolation = "all"
                        elif self.isolation == "all":
                            self.isolation = "only infected"
                    if (x-800)**2 + (y-80)**2 < 15**2:
                        self.amount += 10
                    if (x-770)**2 + (y-80)**2 < 15**2:
                        self.amount -= 10
                    if (x-800)**2 + (y-110)**2 < 15**2:
                        self.rinf += 1
                    if (x-770)**2 + (y-110)**2 < 15**2:
                        self.rinf -= 1
                    if (x-800)**2 + (y-140)**2 < 15**2:
                        self.deathprobability += 5
                    if (x-770)**2 + (y-140)**2 < 15**2:
                        self.deathprobability -= 5
                    if (x-800)**2 + (y-170)**2 < 15**2:
                        self.timetosymptoms += 5
                    if (x-770)**2 + (y-170)**2 < 15**2:
                        self.timetosymptoms -= 5
                    if (x-800)**2 + (y-200)**2 < 15**2:
                        self.timetogetwell += 5
                    if (x-770)**2 + (y-200)**2 < 15**2:
                        self.timetogetwell -= 5
                    if (x-800)**2 + (y-230)**2 < 15**2:
                        self.broun += 1
                    if (x-770)**2 + (y-230)**2 < 15**2:
                        self.broun -= 1
                    if (x-800)**2 + (y-260)**2 < 15**2:
                        self.speed += 0.2
                    if (x-770)**2 + (y-260)**2 < 15**2:
                        self.speed -= 0.2
                    if (x-400)**2 + (y-400)**2 < 75**2:
                        stop = True
                    # я знаю что это ужасно
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

        while not stop:

            screen.fill(WHITE)
            self.button('Население ' + str(self.amount),
                        4, (180, 0, 0), (10, 20))
            self.button('Количество выживших ' + str(len(self.pers)),
                        4, (180, 0, 0), (10, 50))

            self.button('Длительность эпидемии: ' + str(self.time),
                        4, (180, 0, 0), (10, 80))
            self.button('График сохранен figures/figure.png',
                        4, (180, 0, 0), (10, 140))
            self.button('Завершить ',
                        4, (180, 0, 0), (330, 400))
            self.button('Заново ',
                        4, (180, 0, 0), (470, 400))
            if self.time == 0:
                self.button('Вирус убил первого своего носителя,' +
                            ' никого не заразив ',
                            1, (210, 0, 0), (10, 110))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if (x-330)**2 + (y-400)**2 < 75**2:
                        stop = True
                        return True
                    if (x-470)**2 + (y-400)**2 < 75**2:
                        stop = True
                if event.type == pygame.QUIT:
                    stop = True
                    return True
