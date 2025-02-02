import pygame
import sys
import random

#DEPENDE DEL NIVEL
TAMANO_CELDA = 20
ANCHO = 20
ALTO = 15
COLORES = {
    "fondo": (0, 0, 0),
    "serpiente": (0, 255, 0),
    "manzana": (255, 0, 0),
    "bloque": (128, 128, 128),
    "portal": (0, 0, 255)
}
level_map = [
    "####################",
    "#000000000000000000#",
    "#000000000000000000#",
    "#000000000000000000#",
    "#0000000000?0000000#",
    "#000000000?00000000#",
    "#00000000?000000000#",
    "#0000000?0000000000#",
    "#000000?00000000000#",
    "#00000?00000000000@#",
    "####################",
    "####################",
    "####################",
    "####################",
    "####################"
]
mapa = []


#INICIA
pygame.init()
ventana = pygame.display.set_mode((ANCHO * TAMANO_CELDA, ALTO * TAMANO_CELDA))  # Asegurarnos de que el tamaño de la ventana sea correcto
reloj = pygame.time.Clock()

#FUNCIONES
def crear_mapa():
    global mapa
    for fila in level_map:
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
                    pygame.draw.rect(ventana, COLORES["bloque"], (x*TAMANO_CELDA, y*TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
                elif mapa[y][x] == "manzana":
                    pygame.draw.rect(ventana, COLORES["manzana"], (x*TAMANO_CELDA, y*TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
                elif mapa[y][x] == "portal":
                    pygame.draw.rect(ventana, COLORES["portal"], (x*TAMANO_CELDA, y*TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))

def dibujar_serpiente(serpiente):
    for segmento in serpiente:
        pygame.draw.rect(ventana, COLORES["serpiente"], (segmento[0]*TAMANO_CELDA, segmento[1]*TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))

def mover_serpiente(serpiente, direccion):
    global mapa
    cabeza = serpiente[0]
    nueva_cabeza = [cabeza[0] + direccion[0], cabeza[1] + direccion[1]]

    # Verifica colisiones con bloques o el propio cuerpo
    if nueva_cabeza in serpiente or mapa[nueva_cabeza[1]][nueva_cabeza[0]] == "bloque":
        return

    # Mueve la serpiente
    serpiente.insert(0, nueva_cabeza)
    if mapa[nueva_cabeza[1]][nueva_cabeza[0]] != "manzana":
        serpiente.pop()

    

def verificar_gravedad(serpiente, mapa):
    caer = True
    for i, segmento in enumerate(serpiente):
        x, y = segmento
        if y + 1 >= ALTO or mapa[y + 1][x] == "bloque" or mapa[y + 1][x] == "manzana":
            caer = False
    if caer == True:
        for i, segmento in enumerate(serpiente):
            serpiente[i][1] += 1 
        pygame.display.update()
        reloj.tick(10)
        pygame.time.wait(100) 
        print(serpiente[0][1])
        verificar_gravedad(serpiente, mapa)

def verificar_colision_portal(serpiente, mapa):
    cabeza = serpiente[0]
    x, y = cabeza
    if mapa[y][x] == "portal":
        print("¡Has encontrado el portal!")
        return True 
    return False

def verificar_colision_manzana(serpiente, mapa):
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

def crear_nivel():
    mapa = crear_mapa()
    serpiente = [[5, 5]]
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

        if verificar_colision_portal(serpiente, mapa):
            mostrar_mensaje("¡Has ganado!", 2)  
            pygame.quit()  
            sys.exit()

        if verificar_colision_manzana(serpiente, mapa):
            x, y = serpiente[0]
            mapa[y][x] = None  
            serpiente.append([serpiente[-1][0], serpiente[-1][1]])  

        ventana.fill(COLORES["fondo"])
        dibujar_mapa()
        dibujar_serpiente(serpiente)
        verificar_gravedad(serpiente, mapa)
        pygame.display.update()
        reloj.tick(10)

def main():
    crear_nivel()

if __name__ == "__main__":
    main()
