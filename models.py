import pygame
from random import randint

def randch(prob):
    # нужна для обработки вероятности смерти
    N = randint(0, 100)
    if N <= prob:
        return True
    else:
        return False

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

from views import WIDTH, HEIGHT
# если isolation only infected, то изолируем после появления симптомов,
# если no isolation - никого никогда не изолируем,
# если isolation == all - изолируем всех с самого начала
# isolation = "only infected"

class Inf_class:
    def __init__(self, screen: pygame.Surface, amount=100):
        self.pers = []
        # если isolation only infected, то изолируем после появления симптомов,
        # если no isolation - никого никогда не изолируем,
        # если isolation == all - изолируем всех с самого начала
        self.isolation = "no"
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.amount = amount
        self.deathprobability = 25
        # вероятность смерти
        self.screen = screen
        self.rinf = 6
        self.r = 3
        self.timetogetwell = 15
        self.timetosymptoms = 5
        # время до появления симптомов
class Mob(Inf_class):
    def __init__(self,screen, x, y, color=BLACK, probab = 0.01):
        super().__init__(screen)
        self.x = x
        self.y = y
        
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.broun = 10
        # определяет амплитуду броуновского движения
        self.color = BLACK
        self.speed = 0.5
        # скорость отвечающая за то, как далеко ходят люди, от 0 до 1
        self.inf = False
        self.probab = probab        
        self.immu = False
        self.time = 0
        
        self.timeinffirst = 0
        
        self.flag = 0
        
        self.isolated = False
        # Если True, то изолируем его  
    def isolate(self):
        '''Если человек заболел, то изолируем его, когда появятся симптомы
        (флажок isolation = "only infected"),
        либо флажок all - изолируем всех
        no isolation никого
        Делаем оскорость(описанную выше) и 
        амплитуду Броуновского движения нулевой,
        оставляя то, что другие могут к нему приближаться
        (не все соблюдают самоизоляцию)
        Если выздоравливает отменяем
        '''
        if self.isolation == "only infected":
            if self.inf == True:
                if self.time > self.timetosymptoms:
                    self.isolated = True
                    self.broun = 30
                    self.speed = 0
            else:
                self.isolated = False
                self.broun = 10
                self.speed = 0.5
        if self.isolation == "all":
            self.isolated = True
            self.broun = 30
            self.speed = 0
                # можно было бы это возвращать к значениям,
                # которые ввел пользователь
                
    def die(self, pers):
        if self.inf == True:
            if self.flag == 0:
                if randch(self.deathprobability):  
                    pers.remove(self)
                    return pers
                    
                self.flag = 1
            
                
                
    def draw(self):
        if self.inf:
            
            self.color = RED
            pygame.draw.circle(self.screen, RED, 
                               (self.x, self.y), self.rinf, 1)
        elif self.immu == True:
            self.color = GREEN
        else:
            self.color = BLACK
            
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        
        
    def move(self, dt):
        
        
        self.vx = randint(-10,10)/self.broun + randint(-1, 1)*self.speed
        self.vy = randint(-10,10)/self.broun + randint(-1, 1)*self.speed
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.x = self.x % self.WIDTH
        self.y = self.y % self.HEIGHT
    
    def get_well(self):
        '''
        Функция выздоровления.
        Если время, которое человек болеет больше времени, которое нужно,
        чтобы поправиться, человек выздоравливает
        '''
        if self.time >= self.timetogetwell:
            self.inf = False
            self.immu = True

