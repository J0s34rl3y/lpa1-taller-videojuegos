import random
import pygame
from enemigos import *
from treasure import Treasure

class Escenario:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fondos = {}  # Diccionario de fondos para las áreas
        self.areas = []  # Lista de áreas explorables
        self.escenario_actual = 0  # Índice del escenario actual

    def cargar_fondos(self):
        """Cargar los fondos para las áreas."""
        self.fondos = {
            "meteoros": pygame.image.load("assets/imagenes/fondo_meteoros.png").convert(),
            "enemigos": pygame.image.load("assets/imagenes/fondo_enemigos.png").convert(),
            "tesoros": pygame.image.load("assets/imagenes/fondo_tesoros.png").convert()
        }

    def generar_areas(self):
        """Definir las áreas explorables."""
        self.areas = [
            {"nombre": "Zona de Meteoros", "fondo": self.fondos["meteoros"], "rect": pygame.Rect(0, 0, self.width, self.height)},
            {"nombre": "Zona de Enemigos", "fondo": self.fondos["enemigos"], "rect": pygame.Rect(0, 0, self.width, self.height)},
            {"nombre": "Zona de Tesoros", "fondo": self.fondos["tesoros"], "rect": pygame.Rect(0, 0, self.width, self.height)},
        ]

    def cambiar_escenario(self, nuevo_escenario):
        """Cambiar al escenario especificado."""
        if 0 <= nuevo_escenario < len(self.areas):
            self.escenario_actual = nuevo_escenario

    def generar_elementos(self, meteors, enemies, treasure, meteor_img, enemy_img, tesoro_img):
        """Generar elementos en el escenario actual."""
        meteors.clear()
        enemies.clear()
        treasure.clear()

        area = self.areas[self.escenario_actual]
        if area["nombre"] == "Zona de Meteoros":
            for _ in range(5):
                x = random.randint(area["rect"].left, area["rect"].right - 50)
                y = random.randint(area["rect"].top, area["rect"].bottom - 50)
                meteors.append(Meteor(x, y, "mediano", meteor_img))
        elif area["nombre"] == "Zona de Enemigos":
            for _ in range(3):
                x = random.randint(area["rect"].left, area["rect"].right - 50)
                y = random.randint(area["rect"].top, area["rect"].bottom - 50)
                enemies.append(Enemy(x, y, enemy_img))
        elif area["nombre"] == "Zona de Tesoros":
            for _ in range(2):
                x = random.randint(area["rect"].left, area["rect"].right - 50)
                y = random.randint(area["rect"].top, area["rect"].bottom - 50)
                treasure.append(Treasure(x, y, 100, tesoro_img))

    def dibujar(self, screen):
        """Dibujar el fondo del escenario actual."""
        area = self.areas[self.escenario_actual]
        screen.blit(area["fondo"], area["rect"])