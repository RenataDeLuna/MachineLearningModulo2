# -*- coding: utf-8 -*-
"""ActividadMLModelo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zt0UF1ywIViwJmVXlqUb6n72mC4FzJ8P

Implementación del modelo de regresión lineal.
"""

# Importe de las librerías necesarias para la construcción del modelo. 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Código necesario si obtenemos los datos desde Drive en Google Colab

from google.colab import drive

drive.mount("/content/gdrive")  
!pwd

# Commented out IPython magic to ensure Python compatibility.
# %cd "/content/gdrive/MyDrive/ML"
!ls

# Lectura del archivo .csv

df = pd.read_csv('/content/gdrive/MyDrive/ML/winequality_red.csv')
df

# Verificando si el dataframe está listo para ser utilizado para la creación de un modelo o si no está preprocesado, conteniendo valores nulos. 

df.isna().sum()

# Sabiendo que el Dtaframe está limpio, podemos usarlo para el modelo.

# Separando el DataFrame en variables dependientes (de salida) e independientes (de entrada)

df_y = df.Outcome.values # Categoría del data frame, lo que se quiere predecir. 
df_x = df.drop(["Outcome"],axis=1) # Variables de entrada.

# Escalamos los datos, ya que las columnas se encuentran en diferentes tipos de medición. 

df_x_norm = (df_x - df.mean(axis=0)) / df_x.std(axis = 0)

# Dividiendo los valores para train y test, con un tamaño de test de 20% y de train 80%
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size = 0.2, random_state = 42)

x_train = x_train.T
x_test = x_test.T
y_train = y_train.T
y_test = y_test.T

# Función de la sigmoide, toma un valor entre 0 y 1. Regresa la hipótesis.  

def sigmoid(z):
  y_hat = 1 / (1 + np.exp(-z)) 
  return y_hat

# Inicializando los pesos y el bias. 

def weight_bias(size_df):
  weight_init = np.zeros((size_df,1))
  bias_init = 0

  return weight_init, bias_init

# Función del gradiente, para refinar el modelo, recalculando los pesos y el bias. 

def grad_desc(weight_init, bias_init, x_train, y_hat):

  z = np.dot(weight_init.T, x_train) + bias_init
  y_hat = sigmoid(z)
  loss = (-y_train * np.log(y_hat) - (1 - y_train) * np.log(1 - y_hat)).mean()

  weight_grad = (np.dot(x_train, ((y_hat - y_train).T))) / x_train.shape[1]
  bias_grad = np.sum(y_hat - y_train) / x_train.shape[1]
  return loss, weight_grad, bias_grad

# Función para entrenar el modelo
def train(weight, bias, x_train, y_train, epochs, learning_rate): 
  # repitiendo en el número de epochs
  loss_list = []
  for epoch in range(epochs):
    loss, weight_grad, bias_grad = grad_desc(weight, bias, x_train, y_train)
    loss_list.append(loss)

    # Calculando los pesos y el bias
    weight_p = weight - learning_rate * weight_grad
    bias_p = bias - learning_rate * bias_grad

    return weight_p, bias_p, weight_grad, bias_grad, loss_list

# Función para hacer las predicciones

def pred(weight, bias, x_test):
  z = sigmoid(np.dot(weight.T, x_test) + bias)
  Y_pred = np.zeros((1,x_test.shape[1]))

  for i in range (z.shape[1]):
    if z[0,1] <= 0.5:
      Y_pred[0,i] = 0
    else: 
      Y_pred[0,i] = 1
  return Y_pred

def regression(x_train, y_train, x_test, y_test, epochs , learning_rate):
  
    size =  x_train.shape[0]
    weight_init, bias_init = weight_bias(size)
    
    weight_p, bias_p, weight_grad, bias_grad, loss_list  = train(weight_init, bias_init, x_train, y_train, epochs, learning_rate)
    
    y_prediction_test = pred(weight_p, bias_p, x_test)
    

    
    print("test accuracy: ", (100 - np.mean(np.abs(y_prediction_test - y_test)) * 100), " %")

regression(x_train, y_train, x_test, y_test, 100, 0.01)

regression(x_train, y_train, x_test, y_test, 500, 0.01)

regression(x_train, y_train, x_test, y_test, 1000, 0.01)

regression(x_train, y_train, x_test, y_test, 100, 0.06)