"""
variables usadas en "main.py"
last modification: Mar 16 2025
@authors:LV
"""
import numpy as np 

## se puede usar sets para las constantes
vidas_j = 10     #vidas jugador or maquina     
#tablero_vacio  = np.full((10,10), " ") 
orientacion = ["H", "V"]  #horizontal and vertical
"""
  4 barcos de 1 posición de eslora
  3 barcos de 2 posiciones de eslora
  2 barcos de 3 posiciones de eslora
  1 barco de 4 posiciones de eslora
"""
eslora = { 1: 4, 2: 3 , 3: 2, 4: 1} #eslora: num_barcos