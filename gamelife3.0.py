import pygame
import numpy
import random
import time

class cazador:
    pass

class lobo:
    def __init__(self):
        self.tasaVida = 20
        self.tiempoVida = 0
        self.hambre= 8
        self.probabilidadReproduccion = 0.021;
        
    def newGeneracion(self):
        self.tiempoVida = self.tiempoVida+1
        self.hambre = self.hambre-1
    
    def comer(self):
        self.hambre=8
        
class conejo:
    def __init__(self):
        self.tasaVida = 15
        self.tiempoVida = 0
        self.probabilidadReproduccion = 0.025;
        
    def newGeneracion(self):
        self.tiempoVida = self.tiempoVida+1

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

numero_cazadores = random.randrange(5,10)
numero_lobos = random.randrange(20, 50)
numero_conejos = random.randrange(200, 300)
FPS = 30
velocidad = 0.5
generacion = 0
seleccion = "Casilla Muerta"
Pausa = True

# vacia = 0
# cazador = 1
# lobo = 2
# coneho = 3
estado_casillas = numpy.zeros((casillas_x, casillas_y))
object_casillas = []
for x in range(casillas_x):
    temp = []
    for y in range(casillas_y):
        temp.append(None)
    object_casillas.append(temp)
        
# -----------------------------------------

# llenado casillas inicial--------------------


def colocar(estado):
    x = random.randrange(casillas_x)
    y = random.randrange(casillas_y)
    while estado_casillas[x][y] != 0:
        x = random.randrange(casillas_x)
        y = random.randrange(casillas_y)
    estado_casillas[x][y] = estado
    if(estado == 1):
        object_casillas[x][y] = cazador()
    if(estado == 2):
        object_casillas[x][y] = lobo()
    if(estado == 3):
        object_casillas[x][y] = conejo()


def llenado():
    for i in range(numero_cazadores):
        colocar(1)
    for i in range(numero_lobos):
        colocar(2)
    for i in range(numero_conejos):
        colocar(3)

llenado()
copia_estado_casillas= numpy.copy(estado_casillas)
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
    
    cantidad_conejos = contar_entidades()[2]
    # eventos------------------------------------
    for evento in pygame.event.get():
            
        # terminar el juego-----------------------
        if evento.type == pygame.QUIT:
            gameOver = True
        # ---------------------------------------

        # evento de presionar teclas---------------
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                Pausa = not Pausa
                
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
                object_casillas[x][y]= None
            if seleccion == "Cazador":
                estado_casillas[x][y]=1
                object_casillas[x][y]= cazador()
            if seleccion == "Lobo":
                estado_casillas[x][y]=2
                object_casillas[x][y]= lobo()
            if seleccion == "Conejo":
                estado_casillas[x][y]=3
                object_casillas[x][y]= conejo()
        #--------------------------------------------
        
        
        # ------------------------------------------
        
    if not Pausa:
        generacion += 1
        
        #primero el cazador hace sus movimientos
        for X in range(casillas_x):
            for Y in range(casillas_y):
                
                if(copia_estado_casillas[X][Y]==1):
                    listX = []
                    listY = []
                    listX0 = []
                    listY0 = []
                    for x in range(X-1,X+2):
                        for y in range(Y-1,Y+2):
                            
                            if(x==X and y==Y):
                                pass
                            if(x == casillas_x):
                                x=0
                            if(x==-1):
                                x=casillas_x-1
                            if(y == casillas_y):
                                y=0
                            if(y==-1):
                                y=casillas_y-1
                            if(copia_estado_casillas[x][y]== 2 or copia_estado_casillas[x][y] == 3):
                                listX.append(x)
                                listY.append(y)
                            elif(copia_estado_casillas[x][y]== 0):
                                listX0.append(x)
                                listY0.append(y)
                    if(len(listX)!=0):
                        num = random.randrange(len(listX))
                        if(estado_casillas[listX[num]][listY[num]]!=1):
                            estado_casillas[listX[num]][listY[num]]=1
                            estado_casillas[X][Y] = 0;
                            object_casillas[listX[num]][listY[num]]=object_casillas[X][Y]
                            object_casillas[X][Y] = None
                    elif(len(listX0)!=0):
                        num = random.randrange(len(listX0))
                        if(estado_casillas[listX0[num]][listY0[num]]!=1):
                            estado_casillas[listX0[num]][listY0[num]]=1
                            estado_casillas[X][Y] = 0
                            object_casillas[listX0[num]][listY0[num]]=object_casillas[X][Y]
                            object_casillas[X][Y] = None
                            
        copia_estado_casillas = numpy.copy(estado_casillas)
        
        #proseguimos ahora con el movimiento y reproduccion del lobo
        for X in range(casillas_x):
            for Y in range(casillas_y):
                
                if(copia_estado_casillas[X][Y]==2):
                    if(object_casillas[X][Y].hambre <= 0 or object_casillas[X][Y].tiempoVida >= object_casillas[X][Y].tasaVida):
                        object_casillas[X][Y] = None
                        estado_casillas[X][Y] = 0
                    else:
                        listX = []
                        listY = []
                        listX0 = []
                        listY0 = []
                        for x in range(X-1,X+2):
                            for y in range(Y-1,Y+2):
                                
                                if(x==X and y==Y):
                                    pass
                                if(x == casillas_x):
                                    x=0
                                if(x==-1):
                                    x=casillas_x-1
                                if(y == casillas_y):
                                    y=0
                                if(y==-1):
                                    y=casillas_y-1
                                if(copia_estado_casillas[x][y] == 3):
                                    listX.append(x)
                                    listY.append(y)
                                elif(copia_estado_casillas[x][y]== 0):
                                    if(random.random()<object_casillas[X][Y].probabilidadReproduccion and object_casillas[X][Y].hambre >= 7):
                                        estado_casillas[x][y]=2
                                        object_casillas[x][y] = lobo()
                                    else:
                                        listX0.append(x)
                                        listY0.append(y)
                        if(len(listX)!=0):
                            num = random.randrange(len(listX))
                            if(estado_casillas[listX[num]][listY[num]]!=1 and estado_casillas[listX[num]][listY[num]]!=2 ):
                                estado_casillas[listX[num]][listY[num]]=2
                                estado_casillas[X][Y] = 0;
                                object_casillas[X][Y].newGeneracion()
                                object_casillas[X][Y].comer()
                                object_casillas[listX[num]][listY[num]]=object_casillas[X][Y]
                                object_casillas[X][Y] = None
                        elif(len(listX0)!=0):
                            num = random.randrange(len(listX0))
                            if(estado_casillas[listX0[num]][listY0[num]]!=1 and estado_casillas[listX0[num]][listY0[num]]!=2 ):
                                estado_casillas[listX0[num]][listY0[num]]=2
                                estado_casillas[X][Y] = 0
                                object_casillas[X][Y].newGeneracion()
                                object_casillas[listX0[num]][listY0[num]]=object_casillas[X][Y]
                                object_casillas[X][Y] = None
                        else:
                            object_casillas[X][Y].newGeneracion()
                    
            
        copia_estado_casillas = numpy.copy(estado_casillas)
        
        #proseguimos ahora con el movimiento y reproduccion del conejo
        for X in range(casillas_x):
            for Y in range(casillas_y):
                
                if(copia_estado_casillas[X][Y]==3):
                    if(object_casillas[X][Y].tiempoVida >= object_casillas[X][Y].tasaVida):
                        object_casillas[X][Y] = None
                        estado_casillas[X][Y] = 0
                    else:
                        listX0 = []
                        listY0 = []
                        for x in range(X-1,X+2):
                            for y in range(Y-1,Y+2):
                                
                                if(x==X and y==Y):
                                    pass
                                if(x == casillas_x):
                                    x=0
                                if(x==-1):
                                    x=casillas_x-1
                                if(y == casillas_y):
                                    y=0
                                if(y==-1):
                                    y=casillas_y-1
                                if(copia_estado_casillas[x][y]== 0):
                                    if(random.random() <object_casillas[X][Y].probabilidadReproduccion and cantidad_conejos< 1000):
                                        estado_casillas[x][y]=3
                                        object_casillas[x][y] = conejo()
                                    else:
                                        listX0.append(x)
                                        listY0.append(y)
                        if(len(listX0)!=0):
                            num = random.randrange(len(listX0))
                            if(estado_casillas[listX0[num]][listY0[num]]!=1 and estado_casillas[listX0[num]][listY0[num]]!=2 and estado_casillas[listX0[num]][listY0[num]]!=3 ):
                                estado_casillas[listX0[num]][listY0[num]]=3
                                estado_casillas[X][Y] = 0
                                object_casillas[X][Y].newGeneracion()
                                object_casillas[listX0[num]][listY0[num]]=object_casillas[X][Y]
                                object_casillas[X][Y] = None
                        else:
                            object_casillas[X][Y].newGeneracion()
            
        copia_estado_casillas = numpy.copy(estado_casillas)
        
    
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
    for x in range(casillas_x):
        for y in range(casillas_y):
            polygono = [(x*dimension_cuadricula, (y+1)*dimension_cuadricula),
                        ((x+1)*dimension_cuadricula, (y+1)*dimension_cuadricula),
                        ((x+1)*dimension_cuadricula, (y+2)*dimension_cuadricula),
                        (x*dimension_cuadricula, (y+2)*dimension_cuadricula)]
            if estado_casillas[x][y] == 0:
                pygame.draw.polygon(ventana, gris_oscuro, polygono, 1)
            elif estado_casillas[x][y] == 1:
                pygame.draw.polygon(ventana, rojo, polygono, 0)
            elif estado_casillas[x][y] == 2:
                pygame.draw.polygon(ventana, azul_oscuro, polygono, 0)
            elif estado_casillas[x][y] == 3:
                pygame.draw.polygon(ventana, amarillo, polygono, 0)
        # -------------------------------------------

    if (velocidad < 0):
        velocidad = 0

    time.sleep(velocidad)
    pygame.display.flip()
    reloj.tick(FPS)
    # -------------------------------------------


pygame.quit()
