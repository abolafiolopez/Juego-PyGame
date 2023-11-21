"""
Juego de los marcianos
"""

# Importaciones
import pygame
from random import randint
import math
from pygame import mixer

# Iniciar PyGame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Título, icono y fondo
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("Ficheros\\ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("Ficheros\\fondo.jpg")

# Añadir música de fondo
mixer.music.load("Ficheros\\musica.mp3")
mixer.music.play(-1)

# Variables del jugador
imagen_jugador = pygame.image.load("Ficheros\\cohete.png")
jugador_x = 368
jugador_y = 500
jugador_x_modificado = 0

# Variables del enemigo
imagen_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_modificado = []
enemigo_y_modificado = []
cantidad_enemigos = 8

# Bucle para crear los enemigos
for e in range(cantidad_enemigos):
    imagen_enemigo.append(pygame.image.load("Ficheros\\enemigo.png"))
    enemigo_x.append(randint(0, 736))
    enemigo_y.append(randint(50, 200))
    enemigo_x_modificado.append(0.2)
    enemigo_y_modificado.append(50)

# Variables de la bala
imagen_bala = pygame.image.load("Ficheros\\bala.png")
bala_x = 0
bala_y = 500
bala_x_modificado = 0
bala_y_modificado = 0.5
bala_visible = False

# Variables de la puntuación
puntuacion = 0
fuente_puntuacion = pygame.font.Font("freesansbold.ttf", 32)
texto_puntuacion_x = 10
texto_puntuacion_y = 10

# Variables del texto final
fuente_final = pygame.font.Font("freesansbold.ttf", 40)
texto_final_x = 280
texto_final_y = 200


# Función para mostrar el jugador
def jugador(x, y):
    """
    Muestra al jugdor a partir de una imagen y coordenadas
    """
    pantalla.blit(imagen_jugador, (x, y))


# Función para mostrar el enemigo
def enemigo(x, y, imagen):
    """
    Muestra al enemigo a partir de una imagen y coordenadas
    """
    pantalla.blit(imagen_enemigo[imagen], (x, y))


# Función para disparar la bala
def disparar_bala(x, y):
    """
    Muestra y dispara la bala a partir de una imagen y coordenadas
    """
    global bala_visible
    bala_visible = True
    pantalla.blit(imagen_bala, (x + 16, y + 10))


# Función para detectar colisiones
def detectar_colision(x_1, y_1, x_2, y_2):
    """
    Detecta si hay colisión entre la bala y el enemigo a partir de sus posiciones
    """
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# Función para mostrar la puntuación
def mostrar_puntuacion(x, y):
    """
    Funcion para mostrar la puntuación a partir de un texto y coordenadas
    """
    fuente_texto_puntuacion = fuente_puntuacion.render(f"Puntuación: {puntuacion}", True, (255, 255, 255))
    pantalla.blit(fuente_texto_puntuacion, (x, y))


# Mostrar final del juego
def texto_final(x, y):
    fuente_texto_final = fuente_final.render("GAME OVER", True, (255, 255, 255))
    pantalla.blit(fuente_texto_final, (x, y))


# Bucle para iniciar el juego
ejecucion = True
while ejecucion:

    # Fondo de pantalla
    pantalla.blit(fondo,(0, 0))

    # Bucle para comprobar eventos
    for evento in pygame.event.get():

        # Comprueba si se cierra la ventana
        if evento.type == pygame.QUIT:
            ejecucion = False

        # Comprueba si se presiona una tecla
        if evento.type == pygame.KEYDOWN:

            # Tecla izquierda, mover jugador a la izquierda
            if evento.key == pygame.K_LEFT:
                jugador_x_modificado -= 0.3
            # Tecla derecha, mover jugador a la derecha
            if evento.key == pygame.K_RIGHT:
                jugador_x_modificado += 0.3
            # Tecla espacio, disparar bala
            if evento.key == pygame.K_SPACE:
                if not bala_visible:
                    sonido_bala = mixer.Sound("Ficheros\\disparo.mp3")
                    sonido_bala.play()
                    bala_x = jugador_x
                    disparar_bala(bala_x, jugador_y)

        # Comprueba si la tecla deja de presionarse
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_modificado = 0

    # Modificar ubicación del jugador
    jugador_x += jugador_x_modificado

    # Mantener al jugador dentro de los bordes
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # Modificar ubicación del enemigo
    for e in range(cantidad_enemigos):

        # Fin del juego
        if enemigo_y[e] > 500:
            for i in range(cantidad_enemigos):
                enemigo_y[i] = 1000
            texto_final(texto_final_x, texto_final_y)
            break

        enemigo_x[e] += enemigo_x_modificado[e]

        # Mantener al enemigo dentro de los bordes
        if enemigo_x[e] <= 0:
            enemigo_x_modificado[e] += 0.2
            enemigo_y[e] += enemigo_y_modificado[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_modificado[e] -= 0.2
            enemigo_y[e] += enemigo_y_modificado[e]

        # Verificar colisión
        colision = detectar_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound("Ficheros\\golpe.mp3")
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntuacion += 1
            enemigo_x[e] = randint(0, 736)
            enemigo_y[e] = randint(50, 200)

        # Mostrar enemigo
        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Mostrar bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_modificado

    # Mostrar jugador
    jugador(jugador_x, jugador_y)

    # Mostrar puntuacion
    mostrar_puntuacion(texto_puntuacion_x, texto_puntuacion_y)

    # Actualizar
    pygame.display.update()
