"""
Clase principal
last modification: Mar 28 2025
@authors:LUPE, jORGE, FERNANDO, BORJA
"""
import pygame
from clases import Jugador


print("Bienvenido a Hundir la flota grumete")
pygame.mixer.init()
pygame.mixer.music.load('./ship.mp3')
pygame.mixer.music.play()

def switch(opcion):
    diccionario = {
        1 : instrucciones,
        2 : id_jugador,
        3 : jugar,
        4 : salir
    }
    if opcion > 4:
        print("Ingrese un número del 1 al 4")
    else:
        return diccionario[opcion]()

def instrucciones():
    print("""Instrucciones de Juego:
    - Dos jugadores: tú y la máquina
    - Coloca tus barcos en el tablero
    - Tipos de barcos:
        4 barcos de 1 casilla
        3 barcos de 2 casillas
        2 barcos de 3 casillas
        1 barco de 4 casillas
    - Cada casilla equivale a una vida
    - Dispara por turnos hasta hundir toda la flota rival""")

def id_jugador():
    nombre = input("Introduce tu nombre: ")
    print(f"{nombre}, estamos creando tu tablero...")
    global jugador
    jugador = Jugador(nombre)
    return True

def jugar():
    

    if "jugador" not in globals():
        print("======Primero debes introducir tu nombre (opción 2)===")
        return

    print(f"Empecemos a jugar, {jugador.id}")
    
    jugador.posicionar_barcos()
    maquina = Jugador("MAQUINA")
    maquina.posicionar_barcos()

    count = 0
    while jugador.vidas > 0 and maquina.vidas > 0:
        
        jugador.disparo(maquina)

        if jugador.vidas == 0:
            print(f"HAS PERDIDO {jugador.id} ")
            break

        maquina.disparo_maquina(jugador)

        jugador.imprimir_tableros(maquina)
        count = count +1

        if maquina.vidas == 0:
            print(f"HAS GANADO {jugador.id}, ENHORABUENA")
            break

           
        #===Opcion Salir===
        salir = count%2
        if salir == 0:
            pregunta = int(input("""Indique el número con su decision:
                                 1: Seguir jugando
                                 2: Visualizar marcador
                                 3: Salir del juego
                                 """))
            if pregunta == 1:
                continue
            elif pregunta == 2:
                jugador.marcador(maquina)
                continue
            elif pregunta == 3:
                break     

    if jugador.vidas == 0:
        print(f"Has perdido, {jugador.id}")
    elif maquina.vidas == 0:
        print(f"¡Enhorabuena, {jugador.id}! Has ganado a la máquina.")



def salir():
    print("¡Hasta pronto!")
    exit()



while True:
    print("""Seleccione una opción:
1 - Instrucciones de juego
2 - Introducir nombre
3 - Comenzar a jugar
4 - Salir del juego""")
    try:
        opcion = int(input("> "))
        switch(opcion)
    except ValueError:
        print("Por favor, introduce un número válido.")
