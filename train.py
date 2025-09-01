import os
import pandas as pd
import tensorflow as tf
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

MOVIMIENTOS = ['L','R','U','D']
DATOS = [   
            #"100K",
            #"200K",
            #"500K",
            #"1M",
            "2M"
        ]

def generar_entrenar_modelos(datos):
    for nombre in datos:
        df = pd.read_csv(
            os.path.join("Datasets","snake_"+nombre+".csv")
        )
        
        cols = df.columns
        #Convierto los movimientos ['L','R','U','D'] en [0,1,2,3]
        df = df.dropna(subset=[cols[-1]])
        encoder = LabelEncoder()
        encoder.classes_ = np.array(MOVIMIENTOS)
        df[cols[-1]] = encoder.transform(df[cols[-1]])
        for col in cols[4:-1]: # ["pared_izq","pared_der","pared_ar", "pared_ab", "cuerpo_izq","cuerpo_der","cuerpo_ar","cuerpo_ab"]
            #Convierto los valores boleanos en 0 -> falso, 1 -> verdadero 
            df[col] = df[col].astype(int)

        max_count = df['movimiento'].value_counts().max()  # número de la clase mayoritaria
        dfs = []

        for _, grupo in df.groupby('movimiento'):
            #Duplico aleatoriamente las filas hasta alcanzar max_count
            num_reps = max_count - len(grupo)
            if num_reps > 0:
                grupo_extra = grupo.sample(num_reps, replace=True, random_state=42)
                grupo = pd.concat([grupo, grupo_extra])
            dfs.append(grupo)

        df = pd.concat(dfs).sample(frac=1, random_state=42)  # barajamos

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
        print(f"CREANDO EL MODELO Modelo_{nombre}\n")

        capa_entrada = tf.keras.Input(shape=(len(cols)-1,)) #Capa de entrada con la forma (12,) ya que son 12 atributos
        #Las capas ocultas se prueban a base de prueba y error, no hay una ciencia exacta
        capa_oculta_1 = tf.keras.layers.Dense(256, activation="relu")(capa_entrada)
    
        capa_oculta_2 = tf.keras.layers.Dense(256, activation="relu")(capa_oculta_1)
        capa_oculta_2 = tf.keras.layers.Dropout(0.2)(capa_oculta_2)

        capa_oculta_3 = tf.keras.layers.Dense(128, activation="relu")(capa_oculta_2)
        capa_oculta_3 = tf.keras.layers.Dropout(0.2)(capa_oculta_3)
        
        capa_oculta_4 = tf.keras.layers.Dense(128, activation="relu")(capa_oculta_3)

        
        #La capa de salida tendra 4 neuronas (4 movimientos de la serpiente/clases) y tendra como funcion de activacion softmax que es la mejor para clasificacion multiclase
        capa_salida = tf.keras.layers.Dense(4,activation="softmax")(capa_oculta_4)


        #Monto el modelo
        modelo = tf.keras.Model(inputs=capa_entrada, outputs=capa_salida)
        modelo.compile(optimizer="adam",#Mejor optimizador para clasificacion multiclase
                    loss="sparse_categorical_crossentropy",#Se usa ya que los datos de salida que tengo son enteros (0,1,2,3), en vez de ([1,0,0,0]...)
                    metrics=['sparse_categorical_accuracy'])

        #ENTRENAMIENTO DEL MODELO
        print(f"ENTRENANDO EL MODELO Modelo_{nombre}\n")

        callback = tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss', factor=0.5, patience=5, verbose=1
        )
        early = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss', patience=10, restore_best_weights=True
        )
        history = modelo.fit(x=entreno_x, y=entreno_y, 
                            validation_data=(validacion_x,validacion_y),
                            epochs=100,
                            batch_size=256,
                            shuffle=True,
                            callbacks=[callback,early],
                            verbose=0)


        y_pred = modelo.predict(testeo_x).argmax(axis=1)
        print(classification_report(testeo_y, y_pred, target_names=MOVIMIENTOS))
        print(f"GUARDANDO MODELO Modelo_{nombre}\n")
        modelo.save(os.path.join("Modelos","Modelo_"+nombre))
        print("--------------------------------\n")


def main():
    generar_entrenar_modelos(DATOS)

if __name__ == "__main__":
    main()







'''
Modelo_100K
              precision    recall  f1-score   support

           L       0.81      0.69      0.74      3949
           R       0.80      0.72      0.76      3776
           U       0.74      0.75      0.75      3870
           D       0.68      0.85      0.76      3941

    accuracy                           0.75     15536
   macro avg       0.76      0.75      0.75     15536
weighted avg       0.76      0.75      0.75     15536

Modelo_200K
              precision    recall  f1-score   support

           L       0.72      0.84      0.78      7745
           R       0.98      0.54      0.70      7752
           U       0.66      0.91      0.76      7660
           D       0.77      0.70      0.73      7771

    accuracy                           0.75     30928
   macro avg       0.78      0.75      0.74     30928
weighted avg       0.78      0.75      0.74     30928

Modelo_500K
           L       0.76      0.72      0.74     19361
           R       0.83      0.65      0.73     19410
           U       0.70      0.81      0.75     19464
           D       0.71      0.80      0.76     19353

    accuracy                           0.74     77588
   macro avg       0.75      0.74      0.74     77588
weighted avg       0.75      0.74      0.74     77588

Modelo_1M
              precision    recall  f1-score   support

           L       1.00      0.52      0.68     38859
           R       0.72      0.87      0.79     38721
           U       0.75      0.72      0.73     38956
           D       0.68      0.89      0.77     38671

    accuracy                           0.75    155207
   macro avg       0.79      0.75      0.74    155207
weighted avg       0.79      0.75      0.74    155207

Modelo_2M
              precision    recall  f1-score   support

           L       1.00      0.50      0.67     77239
           R       0.71      0.87      0.78     77678
           U       0.68      0.91      0.78     77592
           D       0.75      0.70      0.72     77401

    accuracy                           0.75    309910
   macro avg       0.78      0.75      0.74    309910
weighted avg       0.78      0.75      0.74    309910
'''