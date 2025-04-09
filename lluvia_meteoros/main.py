import pygame
import random
from constants import *
from weapons import *
from enemigos import *

# Inicializar Pygame y configurar pantalla
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lluvia Meteoros")

# Cargar imágenes
player_img = pygame.image.load("assets/imagenes/nave.png").convert_alpha()
meteor_img = pygame.image.load("assets/imagenes/meteoro.png").convert_alpha()
background_img = pygame.image.load("assets/imagenes/espacio.png").convert()

#redimencionar imagenes 
player_img = pygame.transform.scale(player_img,PLAYER_SIZE)
              
# Configuración del jugador (usamos un rectángulo)
player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE[0] // 2,
                     HEIGHT - PLAYER_SIZE[1] - 10, PLAYER_SIZE[0], PLAYER_SIZE[1])

# Listas de objetos del juego
meteors = []
projectiles = []

# Puntuación y fuente
score = 0
dodged_meteors = 0
destroyed_meteors = 0
font = pygame.font.Font(None, 25)

# Control de tiempo de delay de disparos
last_shot = pygame.time.get_ticks()

#Tiempo de inicio del juego
start_time = pygame.time.get_ticks()

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal del juego
running = True
while running:
    current_time = pygame.time.get_ticks()

    # Procesamiento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Disparo con SPACE, respetando el delay y limitando a 5 proyectiles
            if event.key == pygame.K_SPACE and current_time - last_shot > SHOOT_DELAY:
                if len(projectiles) < 5:
                    # Se asume que la clase es "Projectile" (definida en weapons.py)
                    projectiles.append(Projectile(player.centerx - 2, player.top))
                    

    # Mover al jugador según teclas presionadas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= 5
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += 5
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= 5
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += 5

    # Generación de meteoros (si hay menos de 5)
    if len(meteors) < 5:
        size = random.choice(["grande", "mediano", "pequeño"])
        meteor = Meteor(
            random.randint(0, WIDTH - METEOR_SIZE[size][0]),
            -METEOR_SIZE[size][1],
            size,meteor_img)
        meteors.append(meteor)

    # Actualizar proyectiles
    for projectile in projectiles[:]:
        projectile.move()  # Se asume que en Projectile.py existe un método move()
        if projectile.rect.bottom < 0:
            projectiles.remove(projectile)

    # Actualizar meteoros y detectar colisiones 
    for meteor in meteors[:]:
        meteor.move()  # Se asume que en enemigos.py el meteor se mueve mediante move()
        if meteor.rect.top > HEIGHT:
            meteors.remove(meteor)
            dodged_meteors += 1
            continue

    # Detectar colisiones entre proyectiles y meteoros
        for projectile in projectiles[:]:
            if meteor.rect.colliderect(projectile.rect):
                   # Remover el proyectil y el meteor colisionado
                projectiles.remove(projectile)
                meteors.remove(meteor)
                # Sumar puntos (se asume que el método se llama get_points())
                score += meteor.get_points()
                destroyed_meteors += 1
                # Dividir meteoritos, si aplica según la lógica de la clase Meteor
                new_meteors = meteor.split(meteor_img)
                meteors.extend(new_meteors)
                break  # Salir del bucle interno para evitar errores

    # Detectar colisiones entre el jugador y los meteoros
            if player.colliderect(meteor):
                running = False

    # DIBUJAR: Fondo, jugador, meteoros y proyectiles
    screen.blit(background_img, (0, 0))
    screen.blit(player_img, player)
    
    for meteor in meteors:
        meteor.draw(screen)  # Se asume que la clase Meteor tiene el método draw()
    for projectile in projectiles:
        projectile.draw(screen)  # Se asume que Projectile tiene el método draw()

    #calcular el tiempo del juego
    elapsed_time = (current_time - start_time) //1000
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    
    
    # Mostrar puntuación
    score_text = font.render(f"Puntuación: {score}", True, WHITE)
    time_text = font.render(f"Tiempo {minutes:02d}: {seconds:02d}",True,WHITE)
    dodged_text = font.render(f"Meteoritos esquivados {dodged_meteors}" ,True,WHITE)
    destroyed_text = font.render(f"Meteoritos destruidos {destroyed_meteors}" ,True,WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (10, 35))
    screen.blit(dodged_text, (10, 60))
    screen.blit(destroyed_text, (10, 85))
    
             

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
   