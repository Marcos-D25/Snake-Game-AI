import pandas as pd
import numpy as np
import random as r
import math as mt
'''
Como va a ser el dataset

serpiente | distancia_comida |  movimiento | acertado


serpiente: es el conjunto de coordeenadas que componen la serpiente
distancia_comida : va a ser la distancia euclidea entre la cabeza de la serpiente y la comida
movimiento: es el movimiento que el jugador ha elegido (L,R,U,D)
acertado: 0 si no es acertado, 1 si es acertado
'''

'''
DISTANCIA_COMIDA:
Para sacar la distancia de la comida voy a usar la formula que uso en el crear comida, esto me dará posiciones aleatorias
const randNum = Math.round((Math.random()* max ) / unitSize) * unitSize; 
'''

'''
MOVIMIENTO:
Me lo invento :P
'''

'''
ACERTADO:
El movimiento sera acertado si reduce la distancia
'''
SIZE = 2000000
UNITSIZE = 20
WIDTH = 400
HEIGHT = 400
MOVIMIENTOS = ['L','R','U','D']

data = np.empty(shape=[SIZE,4], dtype=list)

def seleccionar_direccion(dir = 'Random'):
    if dir == 'Random':
        dir = r.choice(MOVIMIENTOS)
    return dir

def genera_choque(serpiente:list[list],coord:list) -> bool:
    #Para ver si genera choque la serpiente con el resto del cuerpo he de ver si coincide en alguna coordenada con otra parte de su cuerpo
    choca = False
    for c_s in serpiente:
        choca = c_s[0] == coord[0] and c_s[1] == coord[1]
        if choca:
            break
    return choca

def movimiento_ilegal(coord:list):
    x = coord[0]
    y = coord[1]
    return x < 0 or x>=WIDTH or y < 0 or y >= HEIGHT

def genera_cuerpo(cuerpo_serpiente:list, direccion = None) -> list:
    cuerpo_x = cuerpo_serpiente[0]
    cuerpo_y = cuerpo_serpiente[1]
    choca = True
    while(choca):
        if direccion != None:
            mov = seleccionar_direccion(direccion)
        else:
            mov = seleccionar_direccion()

        match mov:
            case 'L': return [cuerpo_x-UNITSIZE,cuerpo_y]
            case 'R': return [cuerpo_x+UNITSIZE,cuerpo_y]
            case 'U': return [cuerpo_x,cuerpo_y-UNITSIZE]
            case 'D': return [cuerpo_x,cuerpo_y+UNITSIZE]
        if not genera_choque(serpiente,mov) and not movimiento_ilegal(mov):
            choca = False
    
    return mov
    
def generar_coords(serpiente:list[list]):
    ilegal = True
    while ilegal:
        coords = [r.randrange(0, WIDTH, UNITSIZE), r.randrange(0, HEIGHT, UNITSIZE)]
        if not genera_choque(serpiente,coords) and not movimiento_ilegal(coords):
            ilegal = False
    return coords

def generar_serpiente() -> list[list]:
    long_serp = r.randint(1,20)
    cab_s_x = r.randrange(0, WIDTH, UNITSIZE)
    cab_s_y = r.randrange(0, HEIGHT, UNITSIZE)
    serpiente = [[cab_s_x,cab_s_y]]
    
    for _ in range(1,long_serp):
        cuerpo = genera_cuerpo(serpiente[len(serpiente)-1])
        serpiente.append(cuerpo)
    return serpiente



for i in range (SIZE):
    #Genero la serpiente
    serpiente = generar_serpiente()

    #Genero las coordenadas de la comida
    comida = generar_coords(serpiente)

    #Calculo la distancia entre la cabeza de la serpiente y la comida
    dist_comida = mt.sqrt((comida[0]-serpiente[0][0])**2 + (comida[1]-serpiente[0][1])**2)

    #Me invento el movimiento que va a coger
    movimiento = genera_cuerpo(serpiente[0])
    new_dist_comida = mt.sqrt((comida[0]-movimiento[0])**2 + (comida[1]-movimiento[1])**2)
    #Compruebo si el movimiento es acertado o no
    acertado = 1 if new_dist_comida < dist_comida else 0

    data[i] = [serpiente, dist_comida, movimiento, acertado]

df = pd.DataFrame(data, columns=["pos_serpiente", "pos_comida", "movimiento", "acertado"])
df.to_csv('snake_2M.csv', index=False)

