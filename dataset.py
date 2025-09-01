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

DATOS = [#("100K",100000),
         ("200K",200000),
         ("500K",500000),
         ("1M",1000000),
         ("2M",2000000)
         ]
UNITSIZE = 20
WIDTH = 400
HEIGHT = 400
MOVIMIENTOS = ['L','R','U','D']



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


def generar_dataset(datos):
    
    for tupla in datos:
        data = np.empty(shape=[tupla[1],13], dtype=list)
        print(f"GENERANDO DATASET {tupla[0]}")
        for i in range (tupla[1]):
            #Genero la serpiente
            serpiente = generar_serpiente()

            #Genero las coordenadas de la comida
            comida = generar_coords(serpiente)

            #Calculo la distancia entre la cabeza de la serpiente y la comida
            dist_comida_x = abs(comida[0]-serpiente[0][0])
            dist_comida_y = abs(comida[1]-serpiente[0][1])

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
                    nueva_dist_com_x = abs(comida[0]-mov[0])
                    nueva_dist_com_y = abs(comida[1]-mov[1])
                    resultados[2] = nueva_dist_com_x+nueva_dist_com_y
                
                direcciones[dir] = resultados
            #print(f"El conjunto de direcciones es {direcciones}")
            #Veo cual de los movimientos es el mejor 
            valores = list(direcciones.values())
            try:
                dist_comidas = min([pos[2] for pos in valores if not pos[0] and not pos[1]])#Obtengo la minima distancia hacia la comida
                # Encuentra la dirección (key) cuyo valor[2] es igual a dist_comidas
                for dir, val in direcciones.items():
                    if val[2] == dist_comidas:
                        mejor_movimiento = dir
                        break
            except ValueError:
                mejor_movimiento = None
            #print(f"El mejor movimiento es {mejor_movimiento}")
            
            #if i % (tupla[1] // 100) == 0 or i == tupla[1] - 1:
            #    progress = int((i + 1) / tupla[1] * 100)
            #    print(f"\rProgreso del dataset {tupla[0]}: {progress}% [{'#' * (progress // 2)}{' ' * (50 - progress // 2)}]", end='', flush=True)
            
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
        df.to_csv('Datasets/snake_'+tupla[0]+'.csv', index=False)
        print(f"DATASET {tupla[0]} COMPLETADO")
        print("-------------------------------------------")



def main():
    generar_dataset(DATOS)
if __name__ == "__main__":
    main()