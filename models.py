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
        self.speed = 0.5
        # время до появления симптомов
    def options_window(self, screen):
                
        screen.fill(WHITE)
        stop = 0
        f1 = pygame.font.Font(None, 36)
        while not stop:
            screen.fill(WHITE)
            #dt = clock.tick()             
            
            
            
            text1 = f1.render('Самоизоляция ' + str(self.isolation), 4, (180, 0, 0))
            text2 = f1.render('Количество ' + str(self.amount), 4, (180, 0, 0))
            text3 = f1.render('Радиус инфицирования ' + str(self.rinf), 4, (180, 0, 0))
            text4 = f1.render('Вероятность смерти ' + str(self.deathprobability),
                              4, (180, 0, 0))
            text5 = f1.render('Время до появления симптомов ' + str(self.timetosymptoms),
                              4, (180, 0, 0))
            text6 = f1.render('Время до выздоровления ' + str(self.timetogetwell),
                              4, (180, 0, 0))
            text7 = f1.render('Амплитуда Броуновского движения(>0) ' + str(self.broun),
                              4, (180, 0, 0))
            text8 = f1.render('Люди ходят в гости/посещают другие города (0-2)' + str(self.speed),
                              4, (180, 0, 0))
            
            textbutp = f1.render('+ ', 4, (180, 0, 0))
            textbutm = f1.render('-', 4, (180, 0, 0))
            
            
            screen.blit(text1, (10, 50))
            screen.blit(textbutp, (800, 50))
            screen.blit(textbutm, (770, 50))
            screen.blit(text2, (10, 80))
            screen.blit(textbutp, (800, 80))
            screen.blit(textbutm, (770, 80))
            screen.blit(text3, (10, 110))
            screen.blit(textbutp, (800, 110))
            screen.blit(textbutm, (770, 110))
            screen.blit(text4, (10, 140))
            screen.blit(textbutp, (800, 140))
            screen.blit(textbutm, (770, 140))
            screen.blit(text5, (10, 170))
            screen.blit(textbutp, (800, 170))
            screen.blit(textbutm, (770, 170))
            screen.blit(text6, (10, 200))
            screen.blit(textbutp, (800, 200))
            screen.blit(textbutm, (770, 200))
            screen.blit(text7, (10, 230))
            screen.blit(textbutp, (800, 230))
            screen.blit(textbutm, (770, 230))
            screen.blit(text8, (10, 260))
            screen.blit(textbutp, (800, 260))
            screen.blit(textbutm, (770, 260))
            
            ok = f1.render('старт ', 4, (180, 0, 0))
            screen.blit(ok, (400, 400))
            
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    
                    # print(x,y)
                    if (x-800)**2 + (y-50)**2 < 15**2:
                        
                        if self.isolation == "no":
                            self.isolation = "only infected"
                        elif self.isolation == "only infected":
                            self.isolation = "all"
                        elif self.isolation == "all":
                            self.isolation = "no"
                            
                        # я знаю что это ужасно
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
                    #я знаю что это ужасно
                if event.type == pygame.QUIT:
                    stop = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        stop = True
            pygame.display.update()
class Mob(Inf_class):
    def __init__(self,screen, x, y, color=BLACK):
        super().__init__(screen)
        self.x = x
        self.y = y
        
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

