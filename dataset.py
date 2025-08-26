import pandas as pd
import numpy as np
import random as r
import math as mt
'''
Como va a ser el dataset

cabeza_serpiente_x | cabeza_serpiente_y | dist_comida_x | dist_comida_y | pared_arriba | pared_abajo | pared_derecha | pared_izquierda | cuerpo_abajo | cuerpo_arriba | cuerpo_derecha | cuerpo_izquierda


serpiente: es el conjunto de coordeenadas que componen la serpiente
distancia_comida : va a ser la distancia euclidea entre la cabeza de la serpiente y la comida
movimiento: es el movimiento acertado que el jugador ha elegido (L,R,U,D)
'''

'''
DISTANCIA_COMIDA:
Para sacar la distancia de la comida voy a usar la formula que uso en el crear comida, esto me dará posiciones aleatorias
const randNum = Math.round((Math.random()* max ) / unitSize) * unitSize; 
'''

'''
MOVIMIENTO:
Veo el mejor movimiento para llegar mas rapido de manera segura a la comida
'''

SIZE = 10
UNITSIZE = 20
WIDTH = 400
HEIGHT = 400
MOVIMIENTOS = ['L','R','U','D']

data = np.empty(shape=[SIZE,12], dtype=list)


#Devuelve True si la serpiente con el resto de su cuerpo
def genera_choque(serpiente:list[list],coord:list) -> bool:
    choca = False
    for c_s in serpiente:
        choca = c_s[0] == coord[0] and c_s[1] == coord[1]
        if choca:
            break
    return choca

#Devuelve True si se colisiona cualquier coordenada con los bordes
def choca_bordes(coord:list):
    x = coord[0]
    y = coord[1]
    return x < 0 or x>=WIDTH or y < 0 or y >= HEIGHT

#Simula la accion de moverse a un lado determinado
def simular_movimiento(cuerpo_x:int, cuerpo_y:int, dir:str, serpiente:list[list]) -> (list,bool):
    match dir:
        case 'L': mov = [cuerpo_x-UNITSIZE,cuerpo_y]
        case 'R': mov = [cuerpo_x+UNITSIZE,cuerpo_y]
        case 'U': mov = [cuerpo_x,cuerpo_y-UNITSIZE]
        case 'D': mov = [cuerpo_x,cuerpo_y+UNITSIZE]
    if not genera_choque(serpiente,mov) and not choca_bordes(mov):
        choca = False
    else:
        choca = True
    
    return (mov, choca)


#Genera un trozo de cuerpo de la serpiente de manea aleatoria pero que es posible
def genera_cuerpo(serpiente:list) -> list:
    cuerpo_x = serpiente[len(serpiente)-1][0]
    cuerpo_y = serpiente[len(serpiente)-1][1]
    choca = True
    while(choca):
        dir = r.choice(MOVIMIENTOS)
        mov, choca = simular_movimiento(cuerpo_x,cuerpo_y, dir, serpiente)
        
    return mov

#Genera unas coordenadas aleatorias posibles en el tablero
def generar_coords(serpiente:list[list]):
    ilegal = True
    while ilegal:
        coords = [r.randrange(0, WIDTH, UNITSIZE), r.randrange(0, HEIGHT, UNITSIZE)]
        if not genera_choque(serpiente,coords) and not choca_bordes(coords):
            ilegal = False
    return coords

#Genera la serpiente entera
def generar_serpiente() -> list[list]:
    long_serp = r.randint(1,5)
    cab_s_x = r.randrange(0, WIDTH, UNITSIZE)
    cab_s_y = r.randrange(0, HEIGHT, UNITSIZE)
    serpiente = [[cab_s_x,cab_s_y]]
    
    for _ in range(1,long_serp):
        cuerpo = genera_cuerpo(serpiente)
        serpiente.append(cuerpo)
    return serpiente



for i in range (SIZE):
    #Genero la serpiente
    serpiente = generar_serpiente()

    #Genero las coordenadas de la comida
    comida = generar_coords(serpiente)

    #Calculo la distancia entre la cabeza de la serpiente y la comida
    dist_comida = mt.sqrt((comida[0]-serpiente[0][0])**2 + (comida[1]-serpiente[0][1])**2)

    #Calculo el movimiento mejor para llegar a la comida de manera legal
    mov_disponibles = dict()#{dir: [mov, dist]}
    for dir in MOVIMIENTOS:
        mov, choca = simular_movimiento(serpiente[0][0], serpiente[0][1], dir, serpiente)
        if not choca:
            mov_disponibles[dir] = [mt.sqrt((comida[0]-mov[0])**2 + (comida[1]-mov[1])**2)]
    #Veo cual de los movimientos elegidos es el mejor 
    
    min_dist = min(mov_disponibles.values())
    movimiento = [d for d in mov_disponibles.keys() if mov_disponibles[d] == min_dist][0]


    data[i] = [serpiente, dist_comida, movimiento]

df = pd.DataFrame(data, columns=["cabeza_serpiente_x","cabeza_serpiente_y",
                                  "dist_comida_x", "dist_comida_y", 
                                  "pared_arriba" , "pared_abajo" , "pared_derecha" , "pared_izquierda" ,
                                   "cuerpo_arriba" , "cuerpo_abajo" , "cuerpo_derecha" , "cuerpo_izquierda"])
#df.to_csv('snake_2M.csv', index=False)
print(df)
