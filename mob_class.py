import pygame
from random import randint
from my_random import randch


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

class Mob():
    
    def __init__(self, r,screen, x, y, color=BLACK):
        self.r = r
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.x = x
        self.y = y
        self.screen = screen
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        
        
        self.color = BLACK
        
        
        self.inf = False
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
                
    def die(self, pers, time, time2):
        if self.inf == True:
            if randch(50):
                statement = True
                # люди умирают в разное время болезни
            else:
                statement = (time - self.timeinffirst > time2)
            if self.flag == 0 and statement:
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

