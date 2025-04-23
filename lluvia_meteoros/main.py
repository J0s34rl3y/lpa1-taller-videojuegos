import pygame
import random
from constants import *
from weapons import *
from enemigos import *
from powerups import *
from treasure import *  # Asegúrate de tener tesoros.py con la clase Tesoro
from escenarios import Escenario

# Inicializar Pygame y configurar pantalla
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lluvia Meteoros")

# Inicializar el mezclador de sonido de Pygame
pygame.mixer.init()

# Cargar música de fondo
pygame.mixer.music.load("assets/sonidos/musica_fondo.mp3")
pygame.mixer.music.set_volume(0.5)  # Ajustar el volumen de la música
pygame.mixer.music.play(-1)  # Reproducir en bucle infinito

# Cargar efectos de sonido
sound_shoot = pygame.mixer.Sound("assets/sonidos/disparo.wav")
sound_explosion = pygame.mixer.Sound("assets/sonidos/explosion.wav")
sound_collect = pygame.mixer.Sound("assets/sonidos/recolectar.wav")

# Cargar imágenes
player_img = pygame.image.load("assets/imagenes/nave.png").convert_alpha()
meteor_img = pygame.image.load("assets/imagenes/meteoro.png").convert_alpha()
enemy_img = pygame.image.load("assets/imagenes/enemigo.png").convert_alpha()
background_img = pygame.image.load("assets/imagenes/espacio.png").convert()
tesoro_img = pygame.image.load("assets/imagenes/tesoro.png").convert_alpha()  # Imagen del tesoro
life_img = pygame.image.load("assets/imagenes/vida.png").convert_alpha()  # Imagen de vida
# Escalar imágenes si es necesario
player_img = pygame.transform.scale(player_img, PLAYER_SIZE)
tesoro_img = pygame.transform.scale(tesoro_img, (40, 40))  # Ajusta a tu gusto
life_img = pygame.transform.scale(life_img, (30, 30))  # Escalar la imagen de vida

# Lista de fondos y configuraciones por nivel
LEVELS = [
    {"background": "assets/imagenes/espacio.png", "enemy_speed": 2, "enemy_count": 3},  # Fondo principal
    {"background": "assets/imagenes/fondo_meteoros.png", "enemy_speed": 3, "enemy_count": 5},
    {"background": "assets/imagenes/fondo_enemigos.png", "enemy_speed": 4, "enemy_count": 7},
    {"background": "assets/imagenes/fondo_tesoros.png", "enemy_speed": 5, "enemy_count": 10},
    # Agrega más niveles según sea necesario
]

current_level = 0  # Nivel inicial

def load_level(level):
    """Cargar el fondo y configurar enemigos para el nivel actual."""
    global background_img, enemies
    level_config = LEVELS[level]
    background_img = pygame.image.load(level_config["background"]).convert()
    enemies = [
        Enemy(
            random.randint(50, WIDTH - ENEMY_SIZE[0] - 50),
            random.randint(50, 150),
            enemy_img
        )
        for _ in range(level_config["enemy_count"])
    ]
    print(f"Nivel {level + 1} cargado: {level_config}")

def show_level_text(level):
    """Mostrar el texto del nivel actual en pantalla."""
    level_font = pygame.font.Font(None, 74)
    level_text = level_font.render(f"Nivel {level + 1}", True, RED)
    text_rect = level_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(level_text, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)  # Mostrar el texto durante 2 segundos

# Configuración del jugador (usamos un rectángulo)
player = pygame.Rect(
    WIDTH // 2 - PLAYER_SIZE[0] // 2,
    HEIGHT - PLAYER_SIZE[1] - 10,
    PLAYER_SIZE[0],
    PLAYER_SIZE[1]
)
# Función para reiniciar el juego
def restart_game():
    global score, dodged_meteors, destroyed_meteors, lives, meteors, projectiles, powerups, enemies, enemy_projectiles, treasure, collected_treasures, start_time, has_aura, is_invulnerable, cannon_count, aura_start_time, game_over, current_level, falling_lives, particles
    score = 0
    dodged_meteors = 0
    destroyed_meteors = 0
    lives = INITIAL_LIVES
    meteors = []
    projectiles = []
    powerups = []
    enemies = [Enemy(WIDTH // 2 - ENEMY_SIZE[0] // 2, 50, enemy_img)]
    enemy_projectiles = []
    treasure = []
    collected_treasures = []
    has_aura = False
    is_invulnerable = False
    cannon_count = 1
    aura_start_time = 0  # Reinicia el tiempo del aura
    start_time = pygame.time.get_ticks()
    game_over = False  # Asegurarse de que el estado de "Game Over" se reinicie
    current_level = 0  # Reiniciar el nivel
    falling_lives = []  # Reiniciar la lista de vidas recolectables
    particles = []  # Reiniciar la lista de partículas
    load_level(current_level)  # Cargar el primer nivel

# Función para mostrar la pantalla de "Game Over"
def show_game_over():
    global running, game_over
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar el juego
                    restart_game()  # Llama a la función de reinicio
                    return  # Salir de la pantalla de "Game Over"
                elif event.key == pygame.K_ESCAPE:  # Salir del juego
                    running = False
                    game_over = False

        # Fondo semitransparente
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(128)
        s.fill(BLACK)
        screen.blit(s, (0, 0))

        # Texto de "Game Over"
        game_over_font = pygame.font.Font(None, 74)
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        go_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        screen.blit(game_over_text, go_rect)

        # Estadísticas finales
        stats_font = pygame.font.Font(None, 36)
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        final_score = stats_font.render(f"Puntuación final: {score}", True, WHITE)
        time_played = stats_font.render(f"Tiempo Jugado: {minutes:02d}:{seconds:02d}", True, WHITE)
        meteors_dodged = stats_font.render(f"Meteoritos esquivados: {dodged_meteors}", True, WHITE)
        meteors_destroyed = stats_font.render(f"Meteoritos destruidos: {destroyed_meteors}", True, WHITE)

        screen.blit(final_score, (WIDTH / 2 - final_score.get_width() / 2, HEIGHT / 2))
        screen.blit(time_played, (WIDTH / 2 - time_played.get_width() / 2, HEIGHT / 2 + 40))
        screen.blit(meteors_dodged, (WIDTH / 2 - meteors_dodged.get_width() / 2, HEIGHT / 2 + 80))
        screen.blit(meteors_destroyed, (WIDTH / 2 - meteors_destroyed.get_width() / 2, HEIGHT / 2 + 120))

        # Instrucción para reiniciar
        restart_text = stats_font.render("Presiona 'R' para reiniciar", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=(WIDTH / 2, HEIGHT - 100))
        screen.blit(restart_text, restart_text_rect)

        pygame.display.flip()
        clock.tick(60)

# Inicializar variables del juego
meteors = []
projectiles = []
powerups = []
enemies = []
enemy_projectiles = []
treasure = []
collected_treasures = []
falling_lives = []  # Inicializar lista de vidas recolectables
particles = []  # Inicializar lista de partículas
score = 0
dodged_meteors = 0
destroyed_meteors = 0
lives = INITIAL_LIVES
has_aura = False
is_invulnerable = False
has_powerup = False
powerup_start_time = 0
aura_start_time = 0  # Inicializa aura_start_time
font = pygame.font.Font(None, 25)
last_shot = pygame.time.get_ticks()
start_time = pygame.time.get_ticks()
clock = pygame.time.Clock()
paused = False
running = True
game_over = False
cannon_count = 1

# Crear instancia de Escenario
escenario = Escenario(WIDTH, HEIGHT)
escenario.cargar_fondos()
escenario.generar_areas()

# Cargar el fondo para la pantalla de inicio
start_background_img = pygame.image.load("assets/imagenes/fondo_inicio.png").convert()

# Función para activar el aura
def activate_aura():
    global has_aura, aura_start_time
    has_aura = True
    aura_start_time = pygame.time.get_ticks()  # Registrar el tiempo de activación
    print("Aura activada")  # Mensaje de activación

def generate_treasure():
    x = random.randint(0, WIDTH - 30)  # Posición aleatoria en el eje X
    y = random.randint(-100, -50)  # Aparece fuera de la pantalla
    value = random.choice([50, 100, 150])  # Valores monetarios posibles
    return Treasure(x, y, value, tesoro_img)

def generate_life():
    """Generar una vida como objeto recolectable."""
    x = random.randint(0, WIDTH - 30)  # Posición aleatoria en el eje X
    y = random.randint(-100, -50)  # Aparece fuera de la pantalla
    return pygame.Rect(x, y, 30, 30)  # Rectángulo de la vida

def open_shop():
    global collected_treasures, has_aura, cannon_count, lives
    shop_running = True
    while shop_running:
        screen.fill((0, 0, 0))

        # Título de la tienda
        title_font = pygame.font.Font(None, 50)
        title_text = title_font.render("TIENDA", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

        # Opciones de la tienda
        shop_font = pygame.font.Font(None, 36)
        shop_items = [
            "1 - Comprar arma (3 tesoros)",
            "2 - Comprar defensa (2 tesoros)",
            "3 - Comprar vida (1 tesoro)",
            "ESC - Salir"
        ]
        for i, item in enumerate(shop_items):
            item_text = shop_font.render(item, True, WHITE)
            screen.blit(item_text, (50, 100 + i * 40))

        # Mostrar tesoros disponibles
        treasure_text = shop_font.render(f"Tesoros disponibles: {len(collected_treasures)}", True, WHITE)
        screen.blit(treasure_text, (50, 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shop_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    shop_running = False
                elif event.key == pygame.K_1:  # Comprar arma
                    if len(collected_treasures) >= 3:
                        collected_treasures = collected_treasures[3:]
                        cannon_count = 3
                        print("¡Compraste un arma! Ahora disparas con 3 cañones.")
                elif event.key == pygame.K_2:  # Comprar defensa
                    if len(collected_treasures) >= 2 and not has_aura:
                        collected_treasures = collected_treasures[2:]
                        activate_aura()
                        print("¡Aura activada!")
                elif event.key == pygame.K_3:  # Comprar vida
                    if len(collected_treasures) >= 1:
                        collected_treasures = collected_treasures[1:]
                        lives += 1
                        print("¡Compraste una vida!")

def show_start_screen():
    """Mostrar la pantalla de inicio con opciones de Play y Salir."""
    start_running = True
    while start_running:
        # Dibujar el fondo de inicio
        screen.blit(start_background_img, (0, 0))

        # Título del juego
        title_font = pygame.font.Font(None, 74)
        title_text = title_font.render("Lluvia de Meteoros", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        screen.blit(title_text, title_rect)

        # Opciones de inicio
        menu_font = pygame.font.Font(None, 50)
        play_text = menu_font.render("1 - Jugar", True, WHITE)
        exit_text = menu_font.render("2 - Salir", True, WHITE)
        screen.blit(play_text, (WIDTH / 2 - play_text.get_width() / 2, HEIGHT / 2))
        screen.blit(exit_text, (WIDTH / 2 - exit_text.get_width() / 2, HEIGHT / 2 + 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Opción "Jugar"
                    start_running = False
                elif event.key == pygame.K_2:  # Opción "Salir"
                    pygame.quit()
                    exit()

# Mostrar la pantalla de inicio antes de comenzar el juego
show_start_screen()

# Bucle principal del juego
running = True
game_over = False
paused = False
# Llama a restart_game() para la configuración inicial del juego
restart_game()
# Inicializar el primer nivel
load_level(current_level)
# Bucle principal del juego
escenario_actual = 0  # Índice del escenario actual

# Lista para almacenar partículas activas
particles = []

def create_explosion(x, y):
    """Crear partículas de explosión en la posición dada."""
    for _ in range(20):  # Generar 20 partículas
        particles.append(Particle(x, y, (255, 0, 0), random.randint(20, 40)))  # Rojo

def check_victory():
    """Verificar condiciones de victoria."""
    global running
    # Victoria por exploración
    if current_level == len(LEVELS) - 1 and score >= (current_level + 1) * 7000:
        show_victory_screen("¡Victoria por Exploración!")
        running = False

    # Victoria por puntaje
    if score >= 50000:  # Cambia este valor según el puntaje deseado
        show_victory_screen("¡Victoria por Puntaje!")
        running = False

def show_victory_screen(message):
    """Mostrar la pantalla de victoria."""
    victory_running = True
    while victory_running:
        screen.fill(BLACK)

        # Mensaje de victoria
        victory_font = pygame.font.Font(None, 74)
        victory_text = victory_font.render(message, True, WHITE)
        victory_rect = victory_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(victory_text, victory_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    victory_running = False

def shoot():
    global last_shot
    current_time = pygame.time.get_ticks()
    shoot_delay = SHOOT_DELAY // 4 if has_powerup else SHOOT_DELAY
    if current_time - last_shot > shoot_delay:
        for i in range(cannon_count):
            offset = (i - cannon_count // 2) * 10
            projectiles.append(Projectile(player.centerx + offset, player.top, has_powerup))
        last_shot = current_time
        sound_shoot.play()  # Reproducir sonido de disparo

while running:
    if game_over:
        show_game_over()
        continue

    current_time = pygame.time.get_ticks()

    # Verificar condiciones de victoria
    check_victory()

    # ----------------------------------------------------------------
    # Cambio de nivel basado en la puntuación
    # ----------------------------------------------------------------
    if current_level < len(LEVELS) - 1 and score >= (current_level + 1) * 2000:
        current_level += 1
        load_level(current_level)
        show_level_text(current_level)  # Mostrar el texto del nivel actual
        clock.tick(60)

    # ----------------------------------------------------------------
    # Procesamiento de eventos
    # ----------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_SPACE and not paused:
                shoot()
            if event.key == pygame.K_t:
                open_shop()
            if event.key == pygame.K_1:
                escenario_actual = 0  # Cambiar a "Zona de Meteoros"
            elif event.key == pygame.K_2:
                escenario_actual = 1  # Cambiar a "Zona de Enemigos"
            elif event.key == pygame.K_3:
                escenario_actual = 2  # Cambiar a "Zona de Tesoros"

    # Si el juego está pausado, mostramos mensaje y saltamos la lógica
    if paused:
        pause_text = font.render("JUEGO PAUSADO - Presiona P para continuar", True, WHITE)
        text_rect = pause_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(pause_text, text_rect)
        pygame.display.flip()
        clock.tick(60)
        continue

    # ----------------------------------------------------------------
    # Movimiento del jugador
    # ----------------------------------------------------------------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= 5
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += 5
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= 5
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += 5

    # ----------------------------------------------------------------
    # Generación de meteoros
    # ----------------------------------------------------------------
    if len(meteors) < 5:
        size = random.choice(["grande", "mediano", "pequeño"])
        meteor = Meteor(
            random.randint(0, WIDTH - METEOR_SIZE[size][0]),
            -METEOR_SIZE[size][1],
            size,
            meteor_img
        )
        meteors.append(meteor)

    # ----------------------------------------------------------------
    # Generación de power-ups
    # ----------------------------------------------------------------
    if len(powerups) == 0 and random.random() < 0.05:
        powerup = PowerUp(
            random.randint(0, WIDTH - POWERUP_SIZE[0]),
            -POWERUP_SIZE[1]
        )
        powerups.append(powerup)

    for powerup in powerups[:]:
        powerup.move()
        if powerup.rect.top > HEIGHT:
            powerups.remove(powerup)
            continue
        if player.colliderect(powerup.rect):
            has_powerup = True
            powerup_start_time = current_time
            powerups.remove(powerup)
    if has_powerup and current_time - powerup_start_time > POWERUP_DURATION:
        has_powerup = False

    # ----------------------------------------------------------------
    # Generación de tesoros
     # Generar un tesoro aleatoriamente si no hay más de 3 en pantalla
    if len(treasure) < 3 and random.random() < 0.02:  # Probabilidad del 2%
        new_treasure = generate_treasure()
        treasure.append(new_treasure)

    # Mover y dibujar los tesoros
    for tesoro in treasure[:]:
        tesoro.rect.y += 2  # Velocidad de caída del tesoro
        if tesoro.rect.top > HEIGHT:  # Si el tesoro sale de la pantalla
             treasure.remove(tesoro)
        elif player.colliderect(tesoro.rect):  # Si el jugador recoge el tesoro
            collected_treasures.append(tesoro)  # Agregar el tesoro al inventario
            treasure.remove(tesoro)
            sound_collect.play()  # Reproducir sonido de recolección
    
    # ----------------------------------------------------------------
    # Generación de vidas recolectables
    # ----------------------------------------------------------------
    if len(falling_lives) < 1 and random.random() < 0.01:  # Probabilidad del 1%
        falling_lives.append(generate_life())

    # Mover y dibujar las vidas recolectables
    for life in falling_lives[:]:
        life.y += 2  # Velocidad de caída
        if life.top > HEIGHT:  # Si la vida sale de la pantalla
            falling_lives.remove(life)
        elif player.colliderect(life):  # Si el jugador recoge la vida
            lives += 1
            falling_lives.remove(life)
            print("¡Recogiste una vida!")
    
    # ----------------------------------------------------------------
    # Actualizar enemigos y sus disparos
    # ----------------------------------------------------------------
    for enemy in enemies[:]:
        enemy.move()
        if enemy.should_shoot(current_time):
            enemy_projectiles.append(Projectile(enemy.rect.centerx - 2, enemy.rect.bottom, False))

    # ----------------------------------------------------------------
    # Actualizar proyectiles del jugador
    # ----------------------------------------------------------------
    for projectile in projectiles[:]:
        projectile.move()
        if projectile.rect.bottom < 0:
            projectiles.remove(projectile)
        else:
            for enemy in enemies[:]:
                if enemy.rect.colliderect(projectile.rect):
                    # Crear explosión en la posición del enemigo
                    create_explosion(enemy.rect.centerx, enemy.rect.centery)
                    enemies.remove(enemy)
                    projectiles.remove(projectile)
                    score += 200
                    sound_explosion.play()  # Reproducir sonido de explosión
                    new_enemy = Enemy(
                        random.randint(50, WIDTH - ENEMY_SIZE[0] - 50),
                        50,
                        enemy_img
                    )
                    enemies.append(new_enemy)
                    break

    # ----------------------------------------------------------------
    # Proyectiles de enemigos
    # ----------------------------------------------------------------
    for projectile in enemy_projectiles[:]:
        projectile.rect.y += projectile.speed
        if projectile.rect.top > HEIGHT:
            enemy_projectiles.remove(projectile)
        elif player.colliderect(projectile.rect) and not is_invulnerable:
            enemy_projectiles.remove(projectile)
            lives -= 1
            last_hit_time = current_time
            is_invulnerable = True
            if lives <= 0:
                game_over = True  # Cambiar a pantalla de "Game Over"

    # ----------------------------------------------------------------
    # Actualizar meteoros y detectar colisiones
    # ----------------------------------------------------------------
    for meteor in meteors[:]:
        meteor.move()
        if meteor.rect.top > HEIGHT:
            meteors.remove(meteor)
            dodged_meteors += 1
            continue

        # Colisión proyectil vs meteoro
        for projectile in projectiles[:]:
            if meteor.rect.colliderect(projectile.rect):
                projectiles.remove(projectile)
                meteors.remove(meteor)
                score += meteor.get_points()
                destroyed_meteors += 1
                new_meteors = meteor.split(meteor_img)
                meteors.extend(new_meteors)
                break

        # Colisión jugador vs meteoro
        if not has_aura and player.colliderect(meteor) and not is_invulnerable:
            lives -= 1
            last_hit_time = current_time
            is_invulnerable = True
            meteors.remove(meteor)
            if lives <= 0:
                game_over = True  # Cambiar a pantalla de "Game Over"

# Colisión jugador vs proyectiles enemigos
    for projectile in enemy_projectiles[:]:
        if not has_aura and player.colliderect(projectile.rect) and not is_invulnerable:
            enemy_projectiles.remove(projectile)
            lives -= 1
            last_hit_time = current_time
            is_invulnerable = True
            if lives <= 0:
                game_over = True  # Cambiar a pantalla de "Game Over"

    # Estado del aura
    if has_aura:
        # Verificar si la duración del aura ha expirado
        if current_time - aura_start_time > AURA_DURATION:
            has_aura = False
            print("Aura desactivada")  # Mensaje de desactivación

    if is_invulnerable and current_time - last_hit_time > INVULNERABILITY_TIME:
        is_invulnerable = False

   

    # ----------------------------------------------------------------
    # Dibujado de todos los elementos
    # ----------------------------------------------------------------
   
   
    screen.blit(background_img, (0, 0))

    if has_aura:
        pygame.draw.circle(screen, (0, 0, 255), (player.x + player.width // 2, player.y + player.height // 2), 50, 3)
        screen.blit(player_img, player)

    # Mostrar el número total de tesoros recogidos en pantalla
    treasure_text = font.render(f"Tesoros: {len(collected_treasures)}", True, WHITE)
    screen.blit(treasure_text, (WIDTH - 150, 10))  # Ajusta la posición según tu diseño
    
    # Enemigos y sus disparos
    for enemy in enemies:
        enemy.draw(screen)
        
    for projectile in enemy_projectiles:
        projectile.draw(screen)

    # Power-ups
    for powerup in powerups:
        powerup.draw(screen)

   # Tesoros
    for tesoro in treasure:
        tesoro.draw(screen)
    
    # Dibujar las vidas recolectables
    for life in falling_lives:
        screen.blit(life_img, life)
    
     # Dibujar el aura si está activa
   
    # Jugador (parpadeo si invulnerable)
    if not is_invulnerable or (current_time // 200) % 2:
        screen.blit(player_img, player)
     

    # Meteoros y proyectiles del jugador
    for meteor in meteors:
        meteor.draw(screen)
    for projectile in projectiles:
        projectile.draw(screen)

    # ----------------------------------------------------------------
    # Dibujar y actualizar partículas
    # ----------------------------------------------------------------
    for particle in particles[:]:
        particle.move()
        particle.draw(screen)
        if particle.lifetime <= 0:  # Eliminar partículas que hayan expirado
            particles.remove(particle)

    # ----------------------------------------------------------------
    # HUD: puntuación, tiempo, estadísticas y vidas
    # ----------------------------------------------------------------
    elapsed_time = (current_time - start_time) // 1000
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60

    score_text = font.render(f"Puntuación: {score}", True, WHITE)
    time_text = font.render(f"Tiempo {minutes:02d}:{seconds:02d}", True, WHITE)
    dodged_text = font.render(f"Meteoritos esquivados: {dodged_meteors}", True, WHITE)
    destroyed_text = font.render(f"Meteoritos destruidos: {destroyed_meteors}", True, WHITE)
    lives_text = font.render(f"Vidas: {lives}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (10, 35))
    screen.blit(dodged_text, (10, 60))
    screen.blit(destroyed_text, (10, 85))
    screen.blit(lives_text, (10, 110))

    if has_powerup:
        powerup_text = font.render("¡POWER-UP ACTIVO!", True, RED)
        screen.blit(powerup_text, (10, 135))

    pygame.display.flip()
    clock.tick(60)

# ----------------------------------------------------------------
# Pantalla de Game Over
# ----------------------------------------------------------------





pygame.quit()
