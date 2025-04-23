import pygame
from constants import *

# Clase de proyectiles
class Projectile:
    def __init__(self, x, y, powered = False):
        width = 8 if powered else 4
        height = 15 if powered else 10
        
        self.rect = pygame.Rect(x, y,width,height)
        self.speed = 14 if powered else 7
        self.powered = powered

    def move(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        color = RED if self.powered else YELLOW
        pygame.draw.rect(screen, color, self.rect)
