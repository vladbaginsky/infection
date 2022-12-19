import pygame

from views import RED, BLUE

class Text():
    '''
    but - просто кнопка
    label - кнопка с + и -
    
    '''
    def __init__(self,screen, but_type, text, pos, var=0, delta=0):
        self.f = pygame.font.Font(None, 36)
        self.col = BLUE
        self.num = 4
        self.pos = pos
        self.text = self.f.render(text, self.num, self.col)
        self.text1 = text
        self.but_type = but_type
        self.var = var
        self.delta = delta
        self.screen = screen
        self.pos_x = 10
        self.r = 15
    def label(self):
        
        self.screen.blit(self.text, [self.pos_x, self.pos])
        
    def button_plus(self):
        
        text1 = self.f.render("+", self.num, self.col)
        self.screen.blit(text1, [800, self.pos+5])

    def button_minus(self):
        
        text1 = self.f.render("-", 4, self.col)
        self.screen.blit(text1, [770, self.pos+5])
    
    def draw(self):
        if self.but_type == "but":
            self.label()
        elif self.but_type == "label":
            self.label()
            self.button_plus()
            self.button_minus()
    def new_text(self, var):
        self.var = var
        self.text = self.f.render(self.text1 + str(self.var),
                                  self.num, self.col) 
    def is_tap(self, x, y):
        if self.but_type == "but":
            if (x-self.pos_x)**2 + (y-self.pos)**2 < self.r**2:
                return True
        if self.but_type == "label":
            if (x-770)**2 + (y-self.pos)**2 < self.r**2:
                print(self.pos)
                return '-'
            if (x-800)**2 + (y-self.pos)**2 < self.r**2:
                return '+'
        return False
        
    def tap_processing(self, x, y):
        if self.but_type == "but":
            if self.is_tap(x, y):
                
                return True
        if self.but_type == "label":
            if self.is_tap(x, y) == '+':
                return int(self.var + self.delta)
                #print(1)
            elif self.is_tap(x, y) == '-':
                
                return int(self.var - self.delta)
            else:
                #print(self.var)
                return int(self.var)
            
            
            
            
            
            
            
            
            
            


