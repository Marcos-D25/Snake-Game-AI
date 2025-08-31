import os
import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import LabelEncoder
import random as r
MOVIMIENTOS = ['L','R','U','D']
NUMERO = "2M"
df = pd.read_csv(
    os.path.join("Datasets","snake_"+NUMERO+".csv")
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
capa_entrada = tf.keras.Input(shape=(len(cols)-1,)) #Capa de entrada con la forma (12,) ya que son 12 atributos
#Las capas ocultas se prueban a base de prueba y error, no hay una ciencia exacta
capa_oculta_1 = tf.keras.layers.Dense(32,activation="relu")(capa_entrada)
capa_oculta_2 = tf.keras.layers.Dense(32,activation="relu")(capa_oculta_1)
capa_oculta_3 = tf.keras.layers.Dense(32,activation="relu")(capa_oculta_2)
#La capa de salida tendra 4 neuronas (4 movimientos de la serpiente/clases) y tendra como funcion de activacion softmax que es la mejor para clasificacion multiclase
capa_salida = tf.keras.layers.Dense(4,activation="softmax")(capa_oculta_3)
#Monto el modelo
modelo = tf.keras.Model(inputs=capa_entrada, outputs=capa_salida)
modelo.compile(optimizer="adam",#Mejor optimizador para clasificacion multiclase
               loss="sparse_categorical_crossentropy",#Se usa ya que los datos de salida que tengo son enteros (0,1,2,3), en vez de ([1,0,0,0]...)
               metrics=['accuracy'])
'''
 Layer (type)                Output Shape              Param #
=================================================================
 input_2 (InputLayer)        [(None, 12)]              0

 dense_4 (Dense)             (None, 32)                416

 dense_5 (Dense)             (None, 32)                1056

 dense_6 (Dense)             (None, 32)                1056

 dense_7 (Dense)             (None, 4)                 132

=================================================================
Total params: 2,660
Trainable params: 2,660
Non-trainable params: 0
_________________________________________________________________
'''
#ENTRENAMIENTO DEL MODELO
early_stop = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=15, restore_best_weights=True)
history = modelo.fit(x=entreno_x, y=entreno_y, 
                     validation_data=(validacion_x,validacion_y),
                     epochs=100,
                     batch_size=256,
                     shuffle=True,
                     callbacks=early_stop)

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'], label='Entrenamiento')
plt.plot(history.history['val_accuracy'], label='Validación')
plt.xlabel("Épocas")
plt.ylabel("Precisión")
plt.legend()
plt.show()

loss,acc = modelo.evaluate(x = testeo_x, y = testeo_y, verbose = 0)
print(f"La perdida del modelo es de {loss:.4f} y la precision de {acc:.4f}")

modelo.save(os.path.join("Modelos","Modelo_"+NUMERO))