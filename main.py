import pygame
import sys
import random

# Configuración básica
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRID_SIZE = 40
FPS = 10

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Apple Worm")
clock = pygame.time.Clock()

# Diseño del nivel (matriz)
LEVEL = [
    "################",
    "#..............#",
    "#....@.........#",
    "#..####........#",
    "#..............#",
    "#..............#",
    "#..............#",
    "#.....O........#",
    "#.......0000000#",
    "################"
]

# Convertir nivel a objetos del juego
def parse_level(level):
    platforms = []
    worm_pos = None
    apple_pos = None
    for y, row in enumerate(level):
        for x, cell in enumerate(row):
            if cell == "#":
                platforms.append((x, y))
            elif cell == "@":
                worm_pos = (x, y)
            elif cell == "O":
                apple_pos = (x, y)
    return platforms, worm_pos, apple_pos

platforms, worm_pos, apple_pos = parse_level(LEVEL)

# Gusano
worm = [worm_pos]
direction = (0, 0)  # Sin movimiento inicial

# Funciones de dibujo
def draw_grid():
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

def draw_platforms():
    for platform in platforms:
        x, y = platform
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, BLUE, rect)

def draw_worm():
    for segment in worm:
        x, y = segment
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, GREEN, rect)

def draw_apple():
    if apple_pos:
        x, y = apple_pos
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, rect)

# Movimiento y gravedad
def move_worm():
    global apple_pos
    head_x, head_y = worm[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    # Ignorar colisión si no hay movimiento (dirección es (0, 0))
    if direction == (0, 0):
        return True  # No hay colisión, el juego continúa

    # Colisiones con plataformas y bordes
    if new_head in platforms or new_head[0] < 0 or new_head[1] < 0 or new_head[0] >= WINDOW_WIDTH // GRID_SIZE or new_head[1] >= WINDOW_HEIGHT // GRID_SIZE:
        print(f"Perdió: Colisión en {new_head}")
        return False  # Colisión detectada, el juego termina

    # Colisión con el propio cuerpo
    if new_head in worm:
        print(f"Perdió: Colisión con el cuerpo en {new_head}")
        return False  # Colisión detectada, el juego termina

    # Comer la manzana
    if new_head == apple_pos:
        apple_pos = None  # Manzana desaparece
        worm.append(worm[-1])  # El gusano crece añadiendo una nueva "célula" al final
    else:
        worm.pop()  # Eliminar la cola si no crece

    worm.insert(0, new_head)  # Mover la cabeza del gusano
    return True  # Movimiento exitoso, el juego continúa

def apply_gravity():
    global worm
    for i in range(len(worm)-1, -1, -1):
        x, y = worm[i]
        # Verificar si la parte del cuerpo no tiene plataforma o manzana debajo
        if (x, y+1) not in platforms and (x, y+1) != apple_pos:
            # Si no, mover hacia abajo una casilla
            worm[i] = (x, y+1)

# Generar una nueva manzana
def spawn_apple():
    global apple_pos
    while True:
        x = random.randint(1, len(LEVEL[0]) - 2)
        y = random.randint(1, len(LEVEL) - 2)
        if (x, y) not in platforms and (x, y) not in worm:
            apple_pos = (x, y)
            break

# Bucle principal del juego
running = True
while running:
    screen.fill(WHITE)
    draw_grid()
    draw_platforms()
    draw_worm()
    draw_apple()

    # Eventos de entrada
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Cambiar dirección solo cuando se presiona la tecla
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

            # Mover el gusano una vez por cada pulsación de tecla
            if not move_worm():
                print("¡Perdiste!")
                running = False

    # Aplicar gravedad
    apply_gravity()

    # Generar nueva manzana si es necesario
    if not apple_pos:
        spawn_apple()

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()