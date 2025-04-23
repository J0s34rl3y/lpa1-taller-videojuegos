import pygame
from constants import *
import math
import random  # Importar random para generar partículas

pygame.init()

class Enemy:
    def __init__(self, x, y, image, speed=3):
        self.rect = pygame.Rect(x, y, ENEMY_SIZE[0], ENEMY_SIZE[1])  # Rectángulo del enemigo
        self.image = image  # Imagen original
        self.img = pygame.transform.scale(image, ENEMY_SIZE)  # Imagen escalada
        self.speed = speed  # Velocidad configurable
        self.direction = 1  # 1 para derecha, -1 para izquierda
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1000  # Tiempo entre disparos en milisegundos

    def move(self):
        """Mover al enemigo horizontalmente."""
        self.rect.x += self.speed * self.direction
        if self.rect.right > WIDTH - 20:
            self.direction = -1
        elif self.rect.left < 20:
            self.direction = 1

    def should_shoot(self, current_time):
        """Determinar si el enemigo debe disparar."""
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            return True
        return False

    def draw(self, screen):
        """Dibujar al enemigo en la pantalla."""
        screen.blit(self.img, self.rect)

class Meteor:
    def __init__(self, x, y, size, image):
        self.rect = pygame.Rect(x, y, METEOR_SIZE[size][0], METEOR_SIZE[size][1])  # Rectángulo del meteoro
        self.image = image  # Imagen original
        self.img = pygame.transform.scale(image, METEOR_SIZE[size])  # Imagen escalada
        self.initial_x = x
        self.time = 0
        self.size = size

        # Velocidad basada en el tamaño
        self.speed = {
            "grande": 2,
            "mediano": 3,
            "pequeño": 5
        }[size]

        # Amplitud del zigzag
        self.zigzag_amplitude = {
            "grande": 2.0,
            "mediano": 2.5,
            "pequeño": 3.0
        }[size]

    def move(self):
        # Mover el meteorito hacia abajo según su velocidad
        self.rect.y += self.speed
        # Movimiento horizontal en zigzag
        self.time += 0.1
        offset = math.sin(self.time) * self.zigzag_amplitude
        self.rect.x = self.initial_x + (offset * 10)

    def draw(self, screen):
        # Usar la imagen escalada para dibujar
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
        # Método para obtener los puntos según el tamaño del meteoro
        return {
            "grande": 100,
            "mediano": 50,
            "pequeño": 25
        }[self.size]

class Particle:
    def __init__(self, x, y, color, lifetime):
        """Inicializar una partícula."""
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = lifetime
        self.radius = random.randint(2, 5)  # Tamaño aleatorio de la partícula
        self.speed_x = random.uniform(-2, 2)  # Velocidad horizontal aleatoria
        self.speed_y = random.uniform(-2, 2)  # Velocidad vertical aleatoria

    def move(self):
        """Mover la partícula."""
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1  # Reducir el tiempo de vida

    def draw(self, screen):
        """Dibujar la partícula en la pantalla."""
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
