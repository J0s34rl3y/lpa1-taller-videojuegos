import pygame
from constants import *

class Meteor:
    def __init__(self, x, y, size, image):
        self.size = size
        # Crear el rectángulo con el tamaño especificado desde METEOR_SIZE
        self.rect = pygame.Rect(x, y, METEOR_SIZE[size][0], METEOR_SIZE[size][1])
        # Escalar la imagen al tamaño del meteorito
        self.img = pygame.transform.scale(image, METEOR_SIZE[size])
        # Velocidad basada en el tamaño
        self.speed = {
            "grande": 2,
            "mediano": 3,
            "pequeño": 5
        }[size]

    def move(self):
        # Mover el meteorito hacia abajo según su velocidad
        self.rect.y += self.speed

    def draw(self, screen):
        # Dibujar la imagen escalada en el rectángulo del meteorito
        screen.blit(self.img, self.rect)

    def split(self, image):
        # Al dividir, si es grande o mediano se generan meteoritos más pequeños
        if self.size == "grande":
            return [
                Meteor(self.rect.x - 20, self.rect.y, "mediano", image),
                Meteor(self.rect.x + 20, self.rect.y, "mediano", image)
            ]
        elif self.size == "mediano":
            return [
                Meteor(self.rect.x - 15, self.rect.y, "pequeño", image),
                Meteor(self.rect.x + 15, self.rect.y, "pequeño", image)
            ]
        return []

    def get_points(self):
        # Método renombrado de 'ger_points' a 'get_points' para mayor claridad
        return {
            "grande": 100,
            "mediano": 50,
            "pequeño": 25
        }[self.size]
