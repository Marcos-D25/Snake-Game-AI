import pandas as pd
import numpy as np
import random as r
import math as mt
'''
Como va a ser el dataset

cabeza_serpiente_x | cabeza_serpiente_y | dist_comida_x | dist_comida_y | pared_izq | pared_der | pared_ar | pared_ab | cuerpo_izq | cuerpo_der | cuerpo_ar | cuerpo_ab | movimiento


cabeza_serpiente_(x/y): Coordenadas x e y de la cabeza de la serpiente
dist_comida_(x_y): Distancia en x e y de la comida a la cabeza
pared_(arriba/abajo/derecha/izquierda): 0 si no hay pared en la celda siguiente, 1 en caso contrario
cuerpo_(arriba/abajo/derecha/izquierda): 0 si no hay cuerpo de la serpiente en la siguiente celda, 1 en caso contrario
movimiento: Es el mejor movimiento a escoger en la situacion
'''

SIZE = 2000000
UNITSIZE = 20
WIDTH = 400
HEIGHT = 400
MOVIMIENTOS = ['L','R','U','D']

data = np.empty(shape=[SIZE,13], dtype=list)


#Devuelve True si la serpiente con el resto de su cuerpo
def choque_cuerpo(serpiente:list[list],coord:list) -> bool:
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

#Elige una direccion y cambia las coordenadas
def mover (cuerpo_x:int, cuerpo_y:int, dir:str) -> list[int]:
    match dir:
        case 'L': mov = [cuerpo_x-UNITSIZE,cuerpo_y] 
        case 'R': mov = [cuerpo_x+UNITSIZE,cuerpo_y]
        case 'U': mov = [cuerpo_x,cuerpo_y-UNITSIZE]
        case 'D': mov = [cuerpo_x,cuerpo_y+UNITSIZE]
    return mov

#Simula la accion de moverse a un lado determinado
def simular_movimiento(cuerpo_x:int, cuerpo_y:int, dir:str, serpiente:list[list]) -> (list,bool):
    mov = mover(cuerpo_x,cuerpo_y,dir)
    if not choque_cuerpo(serpiente,mov) and not choca_bordes(mov):
        choca = False
    else:
        choca = True
    
    return (mov, choca)


#Genera un trozo de cuerpo de la serpiente de manea aleatoria pero que es posible
def genera_cuerpo(serpiente:list) -> list:
    cuerpo_x = serpiente[len(serpiente)-1][0]
    cuerpo_y = serpiente[len(serpiente)-1][1]
    mov = MOVIMIENTOS.copy()
    r.shuffle(mov)
    for dir in mov:
        mov, choca = simular_movimiento(cuerpo_x,cuerpo_y, dir, serpiente)
        if not choca:
            break
        
    return mov

#Genera unas coordenadas aleatorias posibles en el tablero
def generar_coords(serpiente:list[list]):
    ilegal = True
    while ilegal:
        coords = [r.randrange(0, WIDTH, UNITSIZE), r.randrange(0, HEIGHT, UNITSIZE)]
        if not choque_cuerpo(serpiente,coords) and not choca_bordes(coords):
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
    dist_comida_x = comida[0]-serpiente[0][0]
    dist_comida_y = comida[1]-serpiente[0][1]

    #Compruebo las paredes cercanas, las colisiones con el cuerpo y si es un movimiento valido
    direcciones = dict()#{dir : [bool (pared), bool (cuerpo), dist_comida]}
    for dir in MOVIMIENTOS:
        resultados = [False,False,0] #[bool (pared), bool (cuerpo), dist_comida]
        mov = mover(serpiente[0][0], serpiente[0][1], dir)
        if choca_bordes(mov):
            resultados[0] = True
        if choque_cuerpo(serpiente,mov):
            resultados[1] = True
        
        if not resultados[0] and not resultados[1]:
            resultados[2] = mt.sqrt((mov[0]-comida[0])**2 + (mov[1]-comida[1])**2)
        
        direcciones[dir] = resultados

    #Veo cual de los movimientos es el mejor 
    valores = list(direcciones.values())
    try:
        dist_comidas = min([pos[2] for pos in valores if pos[2] != 0])#Obtengo la minima distancia hacia la comida
        # Encuentra la dirección (key) cuyo valor[2] es igual a dist_comidas
        for dir, val in direcciones.items():
            if val[2] == dist_comidas:
                mejor_movimiento = dir
                break
    except ValueError:
        mejor_movimiento = None

    # Barra de progreso simple
    if i % (SIZE // 100) == 0 or i == SIZE - 1:
        progress = int((i + 1) / SIZE * 100)
        print(f"\rProgreso: {progress}% [{'#' * (progress // 2)}{' ' * (50 - progress // 2)}]", end='', flush=True)
    
    data[i] = [
        serpiente[0][0], serpiente[0][1],
        dist_comida_x, dist_comida_y,
        direcciones['L'][0], direcciones['R'][0], direcciones['U'][0], direcciones['D'][0],
        direcciones['L'][1], direcciones['R'][1], direcciones['U'][1], direcciones['D'][1],
        mejor_movimiento
    ]


    

df = pd.DataFrame(data, columns=["cabeza_serpiente_x","cabeza_serpiente_y",
                                  "dist_comida_x", "dist_comida_y", 
                                  "pared_izq" , "pared_der" , "pared_ar" , "pared_ab" ,
                                   "cuerpo_izq" , "cuerpo_der" , "cuerpo_ar" , "cuerpo_ab",
                                   "movimiento"])
df.to_csv('Datasets/snake_2M.csv', index=False)
#print(df)
