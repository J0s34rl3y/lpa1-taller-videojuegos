import pygame
from constants import * 


class PowerUp:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,POWERUP_SIZE[0],POWERUP_SIZE [1])
        self.active = False
        self.activation_time = 0
        
        
        
    def move(self,):
        self.rect.y += POWERUP_SPEED
        
    def draw ( self,screen):
        pygame.draw.circle(screen,RED,self.rect.center,POWERUP_SIZE[0 // 2])
    def activate (self,current_time):
        self.activate = True
        self.activation_time = current_time
        
    def is_effect_active (self,current_time):
        if not self.active:
            return False
        return current_time - self.activation_time < POWERUP_DURATION    
    