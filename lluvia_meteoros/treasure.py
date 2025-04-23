import pygame
import random
from constants import *  # Importar constantes necesarias (WIDTH, HEIGHT, etc.)

class Treasure:
    def __init__(self, x, y, value, image):
        self.rect = pygame.Rect(x, y, 30, 30)  # Tamaño del tesoro
        self.value = value  # Valor monetario del tesoro
        self.image = pygame.transform.scale(image, (30, 30))  # Escalar la imagen al tamaño del tesoro

    def draw(self, screen):
        # Dibujar el tesoro en pantalla
        screen.blit(self.image, self.rect)

    def collect(self, player):
        # Incrementar el puntaje del jugador al recolectar el tesoro
        player.score += self.value
        
    