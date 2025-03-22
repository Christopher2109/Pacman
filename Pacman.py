# Importar los módulos necesarios
import pygame
import random
import sys
import tkinter as tk
from tkinter import messagebox

# Inicializar pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)

# Definir el tamaño de cada celda en píxeles
TAMANO_CELDA = 40

# Definir un mapa original pequeño y sencillo
mapa_original = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', 'P', '.', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '#', '#', '.', '#', '#', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '#', '.', 'G', '.', '#', '.', '#'],
    ['#', '.', '#', '#', '#', '#', '#', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '.', '.', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#']
]

# Calcular dimensiones de la pantalla basadas en el tamaño del mapa
width = len(mapa_original[0]) * TAMANO_CELDA
height = len(mapa_original) * TAMANO_CELDA

# Crear la ventana
pantalla = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pac-Man")

# Copiar el mapa original para trabajar con él
mapa = [fila.copy() for fila in mapa_original]

# Inicializar variables globales
puntos = 0
puntos_totales = sum(fila.count('.') for fila in mapa_original)

# Buscar la posición inicial de Pac-Man
posicion_inicial_pacman = None
for y in range(len(mapa_original)):
    for x in range(len(mapa_original[0])):
        if mapa_original[y][x] == 'P':
            posicion_inicial_pacman = (x, y)
            break
    if posicion_inicial_pacman:
        break

# Si no se encuentra la posición inicial, establecer una por defecto
if not posicion_inicial_pacman:
    posicion_inicial_pacman = (1, 1)  # Coordenadas por defecto

# Inicializar la posición de Pac-Man
pac_x, pac_y = posicion_inicial_pacman

# Buscar la posición inicial del fantasma
fantasma_x, fantasma_y = None, None
for y in range(len(mapa_original)):
    for x in range(len(mapa_original[0])):
        if mapa_original[y][x] == 'G':
            fantasma_x, fantasma_y = x, y
            break
    if fantasma_x is not None:
        break

# Si no se encuentra la posición inicial del fantasma, establecer una por defecto
if fantasma_x is None or fantasma_y is None:
    fantasma_x, fantasma_y = 4, 4  # Coordenadas por defecto

# Función para dibujar el mapa
def dibujar_mapa():
    pantalla.fill(NEGRO)
    for y in range(len(mapa)):
        for x in range(len(mapa[0])):
            # Dibujar la celda según su contenido
            if mapa[y][x] == '#':
                pygame.draw.rect(pantalla, AZUL, (x * TAMANO_CELDA, y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
            elif mapa[y][x] == '.':
                pygame.draw.circle(pantalla, BLANCO, (x * TAMANO_CELDA + TAMANO_CELDA // 2, y * TAMANO_CELDA + TAMANO_CELDA // 2), TAMANO_CELDA // 8)
            elif mapa[y][x] == 'P':
                pygame.draw.circle(pantalla, AMARILLO, (x * TAMANO_CELDA + TAMANO_CELDA // 2, y * TAMANO_CELDA + TAMANO_CELDA // 2), TAMANO_CELDA // 2 - 5)
            elif mapa[y][x] == 'G':
                pygame.draw.rect(pantalla, ROJO, (x * TAMANO_CELDA + 5, y * TAMANO_CELDA + 5, TAMANO_CELDA - 10, TAMANO_CELDA - 10))
    
    # Dibujar el puntaje
    font = pygame.font.Font(None, 24)
    texto = font.render(f"Puntos: {puntos}/{puntos_totales}", True, BLANCO)
    pantalla.blit(texto, (10, 10))
    pygame.display.flip()

# Función para reiniciar el juego
def reiniciar_juego():
    """Restablece el estado del juego a sus valores iniciales."""
    global pac_x, pac_y, puntos, mapa, fantasma_x, fantasma_y
    
    # Reiniciar la posición del jugador a la coordenada inicial
    pac_x, pac_y = posicion_inicial_pacman
    
    # Restablecer el puntaje a cero
    puntos = 0
    
    # Volver a cargar el mapa con sus elementos originales
    mapa = []
    for fila in mapa_original:
        mapa.append(fila.copy())
    
    # Restaurar la posición del fantasma
    fantasma_x, fantasma_y = None, None
    for y in range(len(mapa_original)):
        for x in range(len(mapa_original[0])):
            if mapa_original[y][x] == 'G':
                fantasma_x, fantasma_y = x, y
                break
        if fantasma_x is not None:
            break

# Función para mover el personaje principal
def mover_pacman(dx, dy):
    """Mueve el Pac-Man en la dirección dada y actualiza la recolección de puntos."""
    global pac_x, pac_y, puntos, mapa
    
    # Verificar que el movimiento no atraviese paredes
    nueva_x = pac_x + dx
    nueva_y = pac_y + dy
    
    if 0 <= nueva_x < len(mapa[0]) and 0 <= nueva_y < len(mapa):
        if mapa[nueva_y][nueva_x] != '#':
            # Si hay un punto en la nueva posición, incrementar el puntaje
            if mapa[nueva_y][nueva_x] == '.':
                puntos += 1
                mapa[nueva_y][nueva_x] = ' '  # Eliminar el punto del mapa
            
            # Verificar si el fantasma está en la nueva posición
            if nueva_x == fantasma_x and nueva_y == fantasma_y:
                mostrar_game_over()
                return
            
            # Actualizar la posición del jugador en el mapa
            mapa[pac_y][pac_x] = ' '  # Eliminar Pac-Man de la posición anterior
            pac_x, pac_y = nueva_x, nueva_y
            mapa[pac_y][pac_x] = 'P'  # Colocar Pac-Man en la nueva posición
            
            # Verificar si se han recogido todos los puntos
            if puntos == puntos_totales:
                mostrar_victoria()

# Función para mover el fantasma
def mover_fantasma():
    """Mueve el fantasma de forma aleatoria en direcciones permitidas."""
    global fantasma_x, fantasma_y, mapa
    
    # Seleccionar una dirección aleatoria entre arriba, abajo, izquierda o derecha
    direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # (dx, dy) para arriba, abajo, izquierda, derecha
    dx, dy = random.choice(direcciones)
    
    # Comprobar que el movimiento no atraviese paredes
    nueva_x = fantasma_x + dx
    nueva_y = fantasma_y + dy
    
    if 0 <= nueva_x < len(mapa[0]) and 0 <= nueva_y < len(mapa):
        if mapa[nueva_y][nueva_x] != '#':
            # Guardar el contenido actual de la celda a la que se mueve el fantasma
            contenido_celda = mapa[nueva_y][nueva_x]
            
            # Guardar lo que había en la posición actual del fantasma antes de que llegara
            celda_actual = ' '  # Por defecto es un espacio vacío
            if mapa_original[fantasma_y][fantasma_x] == '.':
                # Si en el mapa original había un punto, entonces restauramos el punto
                celda_actual = '.'
                
            # Verificar si el punto ya fue recogido
            if celda_actual == '.' and mapa[fantasma_y][fantasma_x] == 'G':
                for y in range(len(mapa)):
                    for x in range(len(mapa[0])):
                        if mapa[y][x] == '.':
                            # Si todavía hay puntos en el mapa, el punto bajo el fantasma podría haber sido recogido
                            celda_actual = ' '
                            break
            
            # Actualizar la posición del fantasma en el mapa
            mapa[fantasma_y][fantasma_x] = celda_actual
            
            fantasma_x, fantasma_y = nueva_x, nueva_y
            
            # Verificar si el fantasma ha capturado a Pac-Man
            if contenido_celda == 'P':
                mostrar_game_over()
            else:
                mapa[fantasma_y][fantasma_x] = 'G'

# Función para mostrar la pantalla de Game Over
def mostrar_game_over():
    """Muestra la pantalla de Game Over y pregunta si el jugador quiere reiniciar."""
    # Dibujar el mensaje de Game Over en la pantalla
    pantalla.fill(NEGRO)
    font = pygame.font.Font(None, 74)
    texto = font.render("Game Over", True, ROJO)
    pantalla.blit(texto, (width // 2 - texto.get_width() // 2, height // 2 - texto.get_height() // 2))
    pygame.display.flip()
    
    # Esperar un tiempo y preguntar al usuario si desea reiniciar el juego
    pygame.time.wait(2000)  # Esperar 2 segundos
    preguntar_volver_a_jugar("¿Quieres jugar de nuevo?")

# Función para mostrar la pantalla de victoria
def mostrar_victoria():
    """Muestra la pantalla de victoria y pregunta si el jugador quiere reiniciar."""
    # Dibujar el mensaje de Victoria en la pantalla
    pantalla.fill(NEGRO)
    font = pygame.font.Font(None, 74)
    texto = font.render("¡Victoria!", True, AMARILLO)
    pantalla.blit(texto, (width // 2 - texto.get_width() // 2, height // 2 - texto.get_height() // 2))
    pygame.display.flip()
    
    # Esperar un tiempo y preguntar al usuario si desea reiniciar el juego
    pygame.time.wait(2000)  # Esperar 2 segundos
    preguntar_volver_a_jugar("¿Quieres jugar de nuevo?")

# Función para preguntar si el jugador quiere volver a jugar
def preguntar_volver_a_jugar(mensaje):
    """Muestra un cuadro de diálogo preguntando si el jugador quiere volver a jugar."""
    # Crear una ventana emergente con tkinter para mostrar un mensaje de juego terminado
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    
    # Preguntar al usuario si desea jugar nuevamente con opciones "Sí" o "No"
    respuesta = messagebox.askyesno("Fin del juego", mensaje)
    
    # Si el usuario elige "Sí", reiniciar el juego
    if respuesta:
        reiniciar_juego()
    # Si el usuario elige "No", cerrar pygame y terminar el programa
    else:
        pygame.quit()
        sys.exit()

# Bucle principal del juego
def main():
    global pantalla
    reloj = pygame.time.Clock()
    contador_movimiento_fantasma = 0
    
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    mover_pacman(0, -1)
                elif evento.key == pygame.K_DOWN:
                    mover_pacman(0, 1)
                elif evento.key == pygame.K_LEFT:
                    mover_pacman(-1, 0)
                elif evento.key == pygame.K_RIGHT:
                    mover_pacman(1, 0)
                elif evento.key == pygame.K_ESCAPE:
                    ejecutando = False
        
        # Mover el fantasma cada cierto número de frames
        contador_movimiento_fantasma += 1
        if contador_movimiento_fantasma >= 15:  # Ajustar este valor para cambiar la velocidad del fantasma
            mover_fantasma()
            contador_movimiento_fantasma = 0
        
        # Dibujar el mapa
        dibujar_mapa()
        
        # Limitar la velocidad del juego
        reloj.tick(30)
    
    pygame.quit()
    sys.exit()

# Iniciar el juego
if __name__ == "__main__":
    main()