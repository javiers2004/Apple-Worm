import pygame
import sys

# Inicializar pygame para obtener la resolución de la pantalla
pygame.init()
info_pantalla = pygame.display.Info()
ANCHO_PANTALLA = info_pantalla.current_w
ALTO_PANTALLA = info_pantalla.current_h

# Configuración de bloques y tamaño dinámico
TAMANO_CELDA = ANCHO_PANTALLA // 20  # 20 bloques de ancho
ANCHO = 20
ALTO = ALTO_PANTALLA // TAMANO_CELDA


COLORES = {
    "fondo": (83, 208, 248),
    "serpiente": (0, 255, 0),
    "manzana": (255, 0, 0),
    "bloque": (128, 128, 128),
    "portal": (161, 17, 223)
}

# Definir niveles
niveles = [
    {
        "mapa": [
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "0000000?##?00000@000",
            "00000#########000000",
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
        ],
        "serpiente_inicio": [[5, 6]],
        "longitud_inicio": 1
    },
    {
        "mapa": [
            "000000000000000000000",
            "000000000000000000000",
            "000000000##0000000000",
            "000000000##0000000000",
            "000000000##0@00000000",
            "00000###0##0#00000000",
            "000000#00#00#00000000",
            "000000#00000#00000000",
            "000000#0?####00000000",
            "000000##0#00000000000",
            "000000000000000000000",

        ],
        "serpiente_inicio": [[7, 4], [6, 4], [5, 4]],
        "longitud_inicio": 3
    },
    {
        "mapa": [
            "00000000000000000000",            
            "00000000000000000000",
            "00000000000000000000",
            "0000000000000@000000",
            "0000####00000#000000",
            "0000#00#00000#000000",
            "0000#0000?000#000000",
            "0000####000###000000",
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000"
        ],
        "serpiente_inicio": [[6, 3], [5, 3], [4, 3]],
        "longitud_inicio": 3
    },
    {
        "mapa": [
            "00000000000000000000",            
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "00000000000000000000",
            "000000000??000000000",
            "000000000??000000000",
            "0000000######0000000",
            "00000000000000000000",
            "000000000000@0000000",
            "00000000000000000000"
        ],
        "serpiente_inicio": [[7, 6]],
        "longitud_inicio": 1
    }
]

# Variables
nivel_actual = 0
mapa = []

# Cargar imágenes
imagen_manzana = pygame.image.load("manzana.png")
imagen_manzana = pygame.transform.scale(imagen_manzana, (TAMANO_CELDA, TAMANO_CELDA))
imagen_bloque = pygame.image.load("bloque.png")
imagen_bloque = pygame.transform.scale(imagen_bloque, (TAMANO_CELDA, TAMANO_CELDA))

fotogramas_portal = []
num_fotogramas = 5  

for i in range(num_fotogramas):
    imagen = pygame.image.load(f"portal\portalFrame{i+1}.png")
    imagen = pygame.transform.scale(imagen, (TAMANO_CELDA, TAMANO_CELDA))  # Ajusta al tamaño de las celdas
    fotogramas_portal.append(imagen)

indice_fotograma_portal = 0
reloj_portal = pygame.time.get_ticks()  
duracion_fotograma_portal = 100

# Inicializar ventana
ventana = pygame.display.set_mode((ANCHO * TAMANO_CELDA, ALTO * TAMANO_CELDA), pygame.FULLSCREEN)
reloj = pygame.time.Clock()

# Funciones
def crear_mapa():
    global mapa
    mapa.clear()  
    for fila in niveles[nivel_actual]["mapa"]:
        fila_lista = []
        for celda in fila:
            if celda == "#":
                fila_lista.append("bloque")
            elif celda == "0":
                fila_lista.append(None)
            elif celda == "@":
                fila_lista.append("portal")
            elif celda == "?":
                fila_lista.append("manzana")
        mapa.append(fila_lista)
    return mapa

def dibujar_mapa():
    global mapa
    for y in range(ALTO):
        for x in range(ANCHO):
            if x < len(mapa[y]) and y < len(mapa):
                if mapa[y][x] == "bloque":
                    ventana.blit(imagen_bloque, (x * TAMANO_CELDA, y * TAMANO_CELDA))
                elif mapa[y][x] == "manzana":
                    ventana.blit(imagen_manzana, (x * TAMANO_CELDA, y * TAMANO_CELDA))
                elif mapa[y][x] == "portal":
                    dibujar_portal_animado(x, y)

def dibujar_serpiente(serpiente):
    for i, segmento in enumerate(serpiente):
        if i == 0:  
            pygame.draw.rect(ventana, (0, 200, 0), (segmento[0] * TAMANO_CELDA, segmento[1] * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))  # Color más oscuro
        else:
            pygame.draw.rect(ventana, COLORES["serpiente"], (segmento[0] * TAMANO_CELDA, segmento[1] * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))

def dibujar_portal_animado(x, y):
    global indice_fotograma_portal, reloj_portal
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - reloj_portal > duracion_fotograma_portal:
        indice_fotograma_portal = (indice_fotograma_portal + 1) % len(fotogramas_portal)
        reloj_portal = tiempo_actual

    ventana.blit(fotogramas_portal[indice_fotograma_portal], (x * TAMANO_CELDA, y * TAMANO_CELDA))

def mover_serpiente(serpiente, direccion):
    global mapa
    cabeza = serpiente[0]
    nueva_cabeza = [cabeza[0] + direccion[0], cabeza[1] + direccion[1]]

    if nueva_cabeza in serpiente or mapa[nueva_cabeza[1]][nueva_cabeza[0]] == "bloque":
        return

    serpiente.insert(0, nueva_cabeza)
    if mapa[nueva_cabeza[1]][nueva_cabeza[0]] != "manzana":
        serpiente.pop()

def verificar_colision_portal(serpiente):
    cabeza = serpiente[0]
    x, y = cabeza
    if mapa[y][x] == "portal":
        return True 
    return False

def verificar_colision_manzana(serpiente):
    cabeza = serpiente[0]
    x, y = cabeza
    if mapa[y][x] == "manzana":
        return True  
    return False

def mostrar_mensaje(texto, tiempo=2):
    font = pygame.font.SysFont(None, 48)
    mensaje = font.render(texto, True, (255, 255, 255))
    rect = mensaje.get_rect(center=(ANCHO * TAMANO_CELDA / 2, ALTO * TAMANO_CELDA / 2))
    ventana.blit(mensaje, rect)
    pygame.display.update()
    pygame.time.wait(tiempo * 1000)

def verificar_gravedad(serpiente, mapa):
    caer = True
    while caer == True:
        for i, segmento in enumerate(serpiente):
            x, y = segmento
            # Verificar que y + 1 esté dentro del rango del mapa
            if y + 1 >= len(mapa) or mapa[y + 1][x] == "bloque" or mapa[y + 1][x] == "manzana":
                caer = False
        if caer == True:
            for i, segmento in enumerate(serpiente):
                serpiente[i][1] += 1 
            pygame.display.update()
            reloj.tick(10)
            pygame.time.wait(50)
            ventana.fill(COLORES["fondo"])
            dibujar_mapa()
            dibujar_serpiente(serpiente)


        

def crear_nivel():
    global nivel_actual
    mapa = crear_mapa()
    serpiente = niveles[nivel_actual]["serpiente_inicio"][:]
    longitud = niveles[nivel_actual]["longitud_inicio"]
    direccion = [0, 0]
    direccion_pending = [0, 0]

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    direccion_pending = [0, -1]
                elif evento.key == pygame.K_DOWN:
                    direccion_pending = [0, 1]
                elif evento.key == pygame.K_LEFT:
                    direccion_pending = [-1, 0]
                elif evento.key == pygame.K_RIGHT:
                    direccion_pending = [1, 0]

        if direccion_pending != [0, 0]:
            direccion = direccion_pending
            direccion_pending = [0, 0]
            mover_serpiente(serpiente, direccion)

        if verificar_colision_portal(serpiente):
            if nivel_actual < len(niveles) - 1:
                nivel_actual += 1
                mostrar_mensaje("¡Nivel completado!", 2)
                crear_nivel()  # Llamar al siguiente nivel
            else:
                mostrar_mensaje("¡Has completado todos los niveles!", 2)
                pygame.quit()
                sys.exit()

        if verificar_colision_manzana(serpiente):
            x, y = serpiente[0]
            mapa[y][x] = None

        ventana.fill(COLORES["fondo"])
        dibujar_mapa()
        dibujar_serpiente(serpiente)
        verificar_gravedad(serpiente, mapa)
        pygame.display.update()
        reloj.tick(10)

def main():
    global nivel_actual
    nivel_actual = 0
    crear_nivel()

if __name__ == "__main__":
    main()  