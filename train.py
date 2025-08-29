import os
import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import LabelEncoder
import random as r
#Cargo el dataset de 100K de datos
MOVIMIENTOS = ['L','R','U','D']

df = pd.read_csv(
    os.path.join("Datasets","snake_100K.csv")
)

cols = df.columns

for col in cols[4:-1]: # ["pared_izq","pared_der","pared_ar", "pared_ab", "cuerpo_izq","cuerpo_der","cuerpo_ar","cuerpo_ab"]
    #Convierto los valores boleanos en 0 -> falso, 1 -> verdadero 
    df[col] = df[col].astype(int)

#Convierto los movimientos ['L','R','U','D'] en [0,1,2,3]
df[cols[-1]] = df[cols[-1]].fillna(r.choice(MOVIMIENTOS))#Aquellos movimientos que sean imposibles (Nan) lo cambiamos por un movimiento random para mejorar el entrenamiento
encoder = LabelEncoder()
encoder.classes_ = np.array(MOVIMIENTOS)
df[cols[-1]] = encoder.transform(df[cols[-1]])



#Divido los datos en ENTRENAMIENTO, VALIDACION y TESTEO (70/20/10)
entreno = df.iloc[0:int(df.shape[0]*.7)]
validacion = df.iloc[int(df.shape[0]*.7):int(df.shape[0]*.9)]
testeo = df.iloc[int(df.shape[0]*.9):]

#Separo los atributos del valor objetivo en cada monton de datos
entreno_x = entreno[cols[:-1]].values
entreno_y = entreno[cols[-1]].values

validacion_x = validacion[cols[:-1]].values
validacion_y = validacion[cols[-1]].values

testeo_x = testeo[cols[:-1]].values
testeo_y = testeo[cols[-1]].values


#MONTAR LA RED NEURONAL