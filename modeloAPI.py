import os
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, WebSocket
import heapq as h
import random as r
MOVIMIENTOS = ['L','R','U','D']
MODELOS = ["Modelo_100K","Modelo_200K","Modelo_500K","Modelo_1M","Modelo_2M"]
modelo = tf.keras.models.load_model(os.path.join("Modelos",MODELOS[2]))



app = FastAPI()
@app.websocket("/predecir_movimiento")
async def predecir(websocket: WebSocket):
    await websocket.accept()  # aceptar conexión
    while True:
        try:
            estado = await websocket.receive_json()  # recibir datos del cliente
            # Crear el array de entrada para el modelo
            datos = [[
                estado["cabeza_serpiente_x"],
                estado["cabeza_serpiente_y"],
                estado["dist_comida_x"],
                estado["dist_comida_y"],
                estado["pared_izq"],
                estado["pared_der"],
                estado["pared_ar"],
                estado["pared_ab"],
                estado["cuerpo_izq"],
                estado["cuerpo_der"],
                estado["cuerpo_ar"],
                estado["cuerpo_ab"]
            ]]
            # Hacer la predicción
            prediccion = modelo.predict(datos)#Predigo en base a los datos
            #La prediccion tiene una forma asi [prob_1,prob_2,prob_3,prob_4] en el que cada posicion es la probabilidad de que sea ese movimiento
            #Problema, hay veces que cae en un estado de bucle, he de ver si hay 2 opciones que se parezcan mucho y elegir aleatoriamente una
            print(f"DISTANCIA DE COMIDA X {datos[0][2]}, DISTANCIA DE COMIDA Y {datos[0][3]}")
            index = aleatoriedad(prediccion[0])
            print(f"MOVIMIENTO PREDICHO -> {MOVIMIENTOS[index]}, {prediccion[0][index]*100}% PROBABILIDAD")
            await websocket.send_json({"movimiento": MOVIMIENTOS[index]})
        except Exception as e:
            print("Error:", e)
            break

def aleatoriedad (prediccion) -> int:
    n1,n2 = h.nlargest(n=2,
                         iterable=enumerate(prediccion), 
                         key= lambda x : x[1] #La funcion nlargest devuelve los numeros mayores del iterable, pero quiero coger el numero mayor del par (indice,numero)
                         )
    #print(f"LOS MOVIMIENTOS ESCOGIDOS SON {n1} Y {n2}")
    
    rango = 0.05
    if (n1[1]-rango<=n2[1]):
        print("ELIGIENDO AL AZAR")
        return r.choice([n1[0],n2[0]])
    else:
        print("ELIGIENDO EL MAYOR")
        return n1[0]
   