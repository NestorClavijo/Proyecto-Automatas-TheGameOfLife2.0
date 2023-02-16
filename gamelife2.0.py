import pygame
import numpy
import random
import time


pygame.init()

reloj = pygame.time.Clock()

# colores -------------------------------
gris = (181, 173, 153)
blanco = (255, 255, 255)
negro = (0, 0, 0)
gris_oscuro = (131, 131, 131)
rojo = (255, 12, 0)
azul_oscuro = (0, 23, 255)
amarillo = (255, 247, 0)
# -----------------------------------------


# creacion ventana-------------------------
dimension_cuadricula = 20
alto = 600 + dimension_cuadricula
ancho = 1200

casillas_x = ancho//dimension_cuadricula
casillas_y = (alto//dimension_cuadricula)-1

ventana = pygame.display.set_mode((ancho, alto))
ventana.fill(blanco)
# -----------------------------------------

# variables del juego----------------------
fuente = pygame.font.SysFont(name="Arial", size=14, bold=False, italic=False)

numero_cazadores = random.randrange(20, 25)
numero_lobos = random.randrange(60, 70)
numero_conejos = random.randrange(50, 100)
FPS = 30
velocidad = 0.5
generacion = 0
seleccion = "Casilla Muerta"
Pausa = False
animacionPausa = False

# vacia = 0
# cazador = 1
# lobo = 2
# coneho = 3
estado_casillas = numpy.zeros((casillas_x, casillas_y))
# -----------------------------------------

# llenado casillas inicial--------------------


def colocar(estado):
    x = random.randrange(casillas_x)
    y = random.randrange(casillas_y)
    while estado_casillas[x][y] != 0:
        x = random.randrange(casillas_x)
        y = random.randrange(casillas_y)
    estado_casillas[x][y] = estado


def llenado():
    for i in range(numero_cazadores):
        colocar(1)
    for i in range(numero_lobos):
        colocar(2)
    for i in range(numero_conejos):
        colocar(3)


llenado()
# --------------------------------------------

# funcion para contar entidades---------------

def contar_entidades():
    n_cazadores = n_lobos = n_conejos = 0
    for x in range(casillas_x):
        for y in range(casillas_y):
            if estado_casillas[x][y] == 1:
                n_cazadores += 1
            if estado_casillas[x][y] == 2:
                n_lobos += 1
            if estado_casillas[x][y] == 3:
                n_conejos += 1
    return (n_cazadores, n_lobos, n_conejos)

# -------------------------------------------


gameOver = False
while not gameOver:
    # eventos------------------------------------
    eve = pygame.event.get()
    for evento in eve:
            
        # terminar el juego-----------------------
        if evento.type == pygame.QUIT:
            gameOver = True
        # ---------------------------------------

        # evento de presionar teclas---------------
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                Pausa = not Pausa
                animacionPausa = not animacionPausa

            if evento.key == pygame.K_c:
                animacionPausa = not animacionPausa
                ventana.fill(blanco)
                estado_casillas = numpy.zeros()
                llenado()
                
            if evento.key == pygame.K_RIGHT:
                if (velocidad < 0.05):
                    velocidad = 0
                else:
                    velocidad -= 0.05

            if evento.key == pygame.K_LEFT:
                if (velocidad >= 1):
                    velocidad = 1
                else:
                    velocidad += 0.05
                    
            #selecciona que recuadro colocar----------
            if evento.key == pygame.K_0:
                seleccion = "Casilla Muerta"
            if evento.key == pygame.K_1:
                seleccion = "Cazador"
            if evento.key == pygame.K_2:
                seleccion = "Lobo"
            if evento.key == pygame.K_3:
                seleccion = "Conejo"
            #-----------------------------------------
            
        #evento de mause--------------------------
        mouseClick = pygame.mouse.get_pressed()
        if (mouseClick[0]or mouseClick[2]) and Pausa:
            posx, posy = pygame.mouse.get_pos()
            x = int(numpy.floor(posx/dimension_cuadricula))
            y = int(numpy.floor(posy/dimension_cuadricula)-1)
            if seleccion == "Casilla Muerta":
                estado_casillas[x][y]=0
            if seleccion == "Cazador":
                estado_casillas[x][y]=1
            if seleccion == "Lobo":
                estado_casillas[x][y]=2
            if seleccion == "Conejo":
                estado_casillas[x][y]=3
        #--------------------------------------------
        
        
        # ------------------------------------------
        
    if not Pausa:
        if generacion == 0:
            Pausa = True
        generacion += 1
    
    ventana.fill(blanco)

    # texto superior-----------------------------
    numero_cazadores, numero_lobos, numero_conejos = contar_entidades()
    texto_colocar = "Cazadores:"+str(numero_cazadores)+",   Lobos:"+str(numero_lobos)+",   Conejos:"+str(
        numero_conejos)+"          Generacion: " + str(generacion)+"          Seleccion: "+seleccion
    vel = 60
    if velocidad <0.05:
        vel = 60
    else:
        vel = round(1/velocidad, 2)
    texto_colocar+="          Velocidad: " + str(vel)+ "gen/s"
    texto = fuente.render(texto_colocar, True, negro)
    ventana.blit(texto, (1, 3))
    # -------------------------------------------

    # dibujar la cuadricula----------------------

    newGameState = numpy.copy(estado_casillas)
    for x in range(1,(casillas_x-1)):
        for y in range(1,(casillas_y-1)):
            
            if animacionPausa:
                n_humanos = 0
                n_zorros = 0
                n_conejos = 0
                
                for z in range((x-1),(x+2)):
                    for k in range((y-1),(y+2)):
                             
                        if estado_casillas[z,k] == 1 and (z != x or k != y):
                            n_humanos+=1
                        elif estado_casillas[z,k] == 2 and (z != x or k != y):

                            n_zorros+=1
                        elif estado_casillas[z,k] == 3 and (z != x or k != y):
                            n_conejos+=1
                            


                #reglas para los cambios de las celdas 
                if estado_casillas[x,y] == 0 and ( n_conejos >= 2 and n_conejos <= 8 and n_humanos <= 2 and n_zorros <= 7):
                    newGameState[x,y] = 3
                elif estado_casillas[x,y] == 0 and (n_zorros >= 2):
                    newGameState[x,y] = 2
                elif estado_casillas[x,y] == 0 and (n_humanos >= 2 and n_humanos <=3):
                    newGameState[x,y] = 1
                elif estado_casillas[x,y] == 1 and (n_zorros >= 4 or n_humanos >=4):
                    newGameState[x,y] = 0
                elif estado_casillas[x,y] == 2 and (n_zorros >= 4 or n_conejos==8 or n_humanos >= 1):
                    newGameState[x,y] = 0
                elif estado_casillas[x,y] == 3 and (n_zorros >= 1 or n_conejos >= 7 or  n_humanos >= 1):
                    newGameState[x,y] = 0

            polygono = [(x*dimension_cuadricula, (y+1)*dimension_cuadricula),
                        ((x+1)*dimension_cuadricula, (y+1)*dimension_cuadricula),
                        ((x+1)*dimension_cuadricula, (y+2)*dimension_cuadricula),
                        (x*dimension_cuadricula, (y+2)*dimension_cuadricula)]
            if newGameState[x][y] == 0:
                pygame.draw.polygon(ventana, gris_oscuro, polygono, 1)
            elif newGameState[x][y] == 1:
                pygame.draw.polygon(ventana, rojo, polygono, 0)
            elif newGameState[x][y] == 2:
                pygame.draw.polygon(ventana, azul_oscuro, polygono, 0)
            elif newGameState[x][y] == 3:
                pygame.draw.polygon(ventana, amarillo, polygono, 0)
        # -------------------------------------------

    estado_casillas=numpy.copy(newGameState)

    if (velocidad < 0):
        velocidad = 0

    time.sleep(velocidad)
    pygame.display.flip()
    reloj.tick(FPS)
    # -------------------------------------------


pygame.quit()
