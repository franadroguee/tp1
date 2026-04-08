from termcolor import colored
import random
import time
import os

"""
VARIABLES FIJAS DE LA SIMULACION
"""

matriz = {} ###El diccionario que contendra la informacion de cada celda.
matriz_turnosiguiente = {}

muertes_conejos = []
muertes_zorros = []
cantidad_conejos = 0
cantidad_zorros = 0

n = 20 ###tamaño de la grilla

dc = 0.1 ###densidad inicial de conejos. Probabilidad de que una celda empiece con un conejo.
dz = 0.1 ###densidad inicial de zorros. Probabilidad de que una celda empiece con un zorro.
dp = 0.1 ###densidad inicial de pasto. Probabilidad de que una celda vacía (sin animal) empiece con pasto.

ec = 5 ###energía inicial de los conejos y de cada conejo recién nacido.
ez = 12 ###energía inicial de los zorros y de cada zorro recién nacido.

gc = 4 ###energía que gana un conejo al comer pasto.
gz = 8 ###energía que gana un zorro al comer un conejo.

pp = 0.1 ###probabilidad de que en un turno dado el pasto crezca en una celda vacía adyacente.
prc = 0.18 ###probabilidad de que un conejo se reproduzca en un turno dado (si tiene energía suficiente).
prz = 0.18 ###probabilidad de que un zorro se reproduzca en un turno dado (si tiene energía suficiente).

emin = 4 ###energía mínima necesaria para que un animal pueda reproducirse.
tmax = 200 

def comienzo():
    for fila in range(n):
        for columna in range(n):
            probabilidad = random.random() ###Numero float entre 0 y 1 que representa la estadistica
            
            """
            La forma en que esto funciona es: la funcion random.random() devuelve un numero que puede ocupar cualquier punto en el espectro entre el 0 y el 1.
            Entonces, el espectro se divide en areas, como sigue:
            
            Entre 0 y la probabilidad de que crezaca pasto, pasto.
            Entre el borde de la probabilidad de que crezca passto y ese borde sumado a la probabilidad de que comiense con un zorro, zorro.
            etc.
            
            Entonces, suponiendo que la probabilidad de que comienze con pasto sea 0.1, la de zorro 0.2 y la de conejo 0.1:
            
            Si random.random() devuelve un valor entre 0 y 0.1, pasto.
            Si devuelve un valor entre 0.1 y 0.3, zorro.
            Entre 0.3 y 0.4 conejo.
            Mas de 0.4, la celda quedara vacia.
            """
            
            if probabilidad < dc: 
                tipo = {
                    "tipo":    "conejo",
                    "energia": ec,   # energía actual del animal
                    "edad": 0    # cantidad de turnos que lleva vivo
                }
                
            elif probabilidad >= dc and probabilidad < (dc + dz):
                tipo = {
                    "tipo": "zorro",
                    "energia": ez,   # energía actual del animal
                    "edad":    0    # cantidad de turnos que lleva vivo
                }
            elif probabilidad >= (dc + dz) and probabilidad < (dc + dz + dp):
                tipo = 'pasto'
            else:
                tipo = 'None'
            
            matriz[f'{columna} {fila}'] = tipo #Se agrega el valor al diccionario. Por ejemplo, '12 4': 'pasto', (celda en pos. (12, 4) es pasto)
            matriz_turnosiguiente[f'{columna} {fila}'] = tipo
        
    print('')
    
    
def encontrar_vecinas(celda):
    ###Las matrizs vecinas sseran de la forma x +- 1, y +- 1
    x = int(str.split(celda)[0])
    y = int(str.split(celda)[1])
    vecinas = [] ###Vacia la lista
        
    if (x-1) >= 0: ###Controla que la celda no este fuera de la grilla
        vecina = (f'{x-1} {y}')
        vecinas.append(vecina) ###Agrega la celda a la lista, ya que se comprobo que esta dentro de la cuadrilla
            
    if (y-1) >= 0: ###Controla que la celda no este fuera de la grilla
        vecina = (f'{x} {y-1}')
        vecinas.append(vecina)
        
    if (x+1) < n: ###Controla que la celda no este fuera de la grilla
        vecina = (f'{x+1} {y}')
        vecinas.append(vecina)
        
    if (y+1) < n: ###Controla que la celda no este fuera de la grilla
        vecina = (f'{x} {y+1}')
        vecinas.append(vecina)
        
    return vecinas ###Devuelve la lista de matriz vecinas a donde haya sido llamada la funcion

def expansion_pasto(celda): ###Ha de recibir unicamente matriz de PASTO, siendo estas filtradas antes de llamar la funcion
    vecinas_disponibles = []
    matriz_turnosiguiente[celda] = 'pasto'
    for vecina in encontrar_vecinas(celda):
        
        if matriz_turnosiguiente[vecina] == 'None': ###Si la celda no tiene nada, esta dissponible
            vecinas_disponibles.append(vecina)


    if random.random() < pp and vecinas_disponibles != []: ###Hace el calculo estadistico para determinar si crecera pasto o no.
            celda_seleccionada = random.choice(vecinas_disponibles)
            matriz_turnosiguiente[str(celda_seleccionada)] = 'pasto' ###Se remplaza la celda

def movimiento_zorro(celda):
    vecinas_disponibles = [] ###Lista vacia
    zorro = matriz[celda]
    for vecina in encontrar_vecinas(celda):
        if matriz_turnosiguiente[vecina]== 'None': ###Si la celda no tiene nada, esta dissponible
            vecinas_disponibles.append(vecina)
        
        elif matriz_turnosiguiente[vecina]== 'pasto':
            pass
        
        elif matriz_turnosiguiente[vecina]['tipo'] == 'conejo':
            vecinas_disponibles.append(vecina)
    
    if vecinas_disponibles != []:
        
        casilla_seleccionada = random.choice(vecinas_disponibles)
        matriz_turnosiguiente[str(casilla_seleccionada)] = zorro
        matriz_turnosiguiente[celda] = 'None'
    
    else:
        matriz_turnosiguiente[celda] = matriz[celda]


def movimiento_conejo(celda):
    vecinas_disponibles = [] ###Lista vacia
    conejo = matriz[celda]
    for vecina in encontrar_vecinas(celda):
        if matriz_turnosiguiente[vecina]== 'None': ###Si la celda no tiene nada, esta dissponible
            vecinas_disponibles.append(vecina)
        
        elif matriz_turnosiguiente[vecina]== 'pasto':
            vecinas_disponibles.append(vecina)
    
    if vecinas_disponibles != []:
        
        casilla_seleccionada = random.choice(vecinas_disponibles)
        matriz_turnosiguiente[str(casilla_seleccionada)] = conejo
        matriz_turnosiguiente[celda] = 'None'
    
    else:
        matriz_turnosiguiente[celda] = matriz[celda]

            
            

def imprimir():
    columna = 1
    print('|' + '-' * (2*n) + '|\n|', end='')
    for celda in matriz_turnosiguiente:
        
        matriz[celda] = matriz_turnosiguiente[celda]
        
        if matriz_turnosiguiente[celda] == 'pasto':
            print(colored('▓▓', 'green'), end='')
        elif matriz_turnosiguiente[celda] == 'None':
            print('  ', end='')
        elif matriz_turnosiguiente[celda]['tipo'] == 'conejo':
            print(colored('▓▓', 'cyan'), end='')
        elif matriz_turnosiguiente[celda]['tipo'] == 'zorro':
            print(colored('▓▓', 'red'), end='')
        
            
        if columna == n:
            print('|\n|', end='')
            columna = 1
        else:
            columna += 1
    print(('-' * (2 * n)) + '|')

