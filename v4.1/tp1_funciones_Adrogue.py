from termcolor import colored
import random
import time
import os
from copy import deepcopy

"""
VARIABLES FIJAS DE LA SIMULACION
"""
snapshot = [] # tendra la forma [[int, int], str], [[int, int], dict]
matriz = []

muertes_conejos = []
muertes_zorros = []

n = 20 # tamaño de la grilla

dc = 0.2 # densidad inicial de conejos. Probabilidad de que una celda empiece con un conejo.
dz = 0.2 # densidad inicial de zorros. Probabilidad de que una celda empiece con un zorro.
dp = 0.3 # densidad inicial de pasto. Probabilidad de que una celda vacía (sin animal) empiece con pasto.

ec = 10 # energía inicial de los conejos y de cada conejo recién nacido.
ez = 12 # energía inicial de los zorros y de cada zorro recién nacido.

gc = 5 # energía que gana un conejo al comer pasto.
gz = 8 # energía que gana un zorro al comer un conejo.

pp = 0.5 # probabilidad de que en un turno dado el pasto crezca en una celda vacía adyacente.
prc = 0.18 # probabilidad de que un conejo se reproduzca en un turno dado (si tiene energía suficiente).
prz = 0.18 # probabilidad de que un zorro se reproduzca en un turno dado (si tiene energía suficiente).

emin = 4 # energía mínima necesaria para que un animal pueda reproducirse.
tmax = 200 

def encontrar_indice(celda):
    """
    descripcion.
    args:
        celda
    returns:
        indice_celda
    """
    
    if type(celda[1]) == int:    
        cordenadas = celda
        
        
    else:
        cordenadas = celda[0]
    numero = int(cordenadas[0]) + (int(cordenadas[1]) * n)
    return numero

def encontrar_vecinas(celda):
    """
    descripcion.
    args:
        celda
    returns:
        celdas_vecinas ([x, y])
    """
    
    x = celda[0][0]
    y = celda[0][1]
    vecinas = [] ###Vacia la lista
        
    if (x-1) >= 0: ###Controla que la celda no este fuera de la grilla
        vecina = ([x-1, y])
        vecinas.append(vecina) ###Agrega la celda a la lista, ya que se comprobo que esta dentro de la cuadrilla
            
    if (y-1) >= 0: ###Controla que la celda no este fuera de la grilla
        vecina = ([x, y-1])
        vecinas.append(vecina)
        
    if (x+1) < n: ###Controla que la celda no este fuera de la grilla
        vecina = ([x+1, y])
        vecinas.append(vecina)
        
    if (y+1) < n: ###Controla que la celda no este fuera de la grilla
        vecina = ([x, y+1])
        vecinas.append(vecina)
        
    return vecinas ###Devuelve la lista de matriz vecinas a donde haya sido llamada la funcion

def comienzo():
    """
    Descripcion.
    Args:
        None
    Returns:
        matriz
    """
    for fila in range(n):
        for columna in range(n):
            probabilidad = random.random() # numero float entre 0 y 1. 
            if probabilidad < dc: 
                matriz.append([[columna, fila], {
                    "tipo":    "conejo",
                    "energia": ec,   # energía actual del animal
                    "edad": 0    # cantidad de turnos que lleva vivo
                }])
            elif probabilidad < (dc + dz):
                matriz.append([[columna, fila], {
                    "tipo":    "zorro",
                    "energia": ez,   # energía actual del animal
                    "edad": 0    # cantidad de turnos que lleva vivo
                }])
            elif probabilidad < (dc + dz + dp):
                matriz.append([[columna, fila], 'pasto'])
            else:
                matriz.append([[columna, fila], None])
    
    return matriz
    
def expansion_pasto(celda, snapshot):
    """
    descripcion.
    args:
        celda de pasto
        snapshot
    returns:
        indice celda donde crecera pasto
    """
    vecinas = encontrar_vecinas(celda)
    vecinas_disponibles = []
    for vecina in vecinas:
        indice = encontrar_indice(vecina)
        if snapshot[indice][1] == None:
            vecinas_disponibles.append(indice)
            
    if vecinas_disponibles != [] and random.random() < pp:
        return random.choice(vecinas_disponibles)
    else:
        return None

def decision_movimiento(celda, snapshot, muertes_conejos, muertes_zorros):
    """
    descripcion.
    args:
        celda con animal
    returns:
        si el conejo vive, decision movimiento (indice)
        si el conejo muere, None
    """
    
    celda[1]['edad'] += 1
    if celda[1]['tipo'] == 'zorro':
        celda[1]['energia'] -= 2
        # si su energia llega a 0 muere y se registra su edad
        if celda[1]['energia'] <= 0:
            indice = encontrar_indice(celda)
            muertes_zorros.append(celda[1]['edad'])
            matriz[indice][1] = None
            return None

        vecinas = encontrar_vecinas(celda)
        vecinas_disponibles = []
        for vecina in vecinas:
            indice = encontrar_indice(vecina)
            if snapshot[indice][1] == 'pasto' or snapshot[indice][1] == None:
                vecinas_disponibles.append(indice)
        if vecinas_disponibles != []:
            return random.choice(vecinas_disponibles)
        else:
            return None

    if celda[1]['tipo'] == 'conejo':
        celda[1]['energia'] -= 1
        # si su energia llega a 0 muere y se registra su edad
        if celda[1]['energia'] <= 0:
            indice = encontrar_indice(celda)
            muertes_conejos.append(celda[1]['edad'])
            matriz[indice][1] = None
            return None

        vecinas = encontrar_vecinas(celda)
        vecinas_disponibles = []
        for vecina in vecinas:
            indice = encontrar_indice(vecina)
            if snapshot[indice][1] == 'pasto' or snapshot[indice][1] == None:
                vecinas_disponibles.append(indice)
            elif snapshot[indice][1]['tipo'] == 'zorro':
                vecinas_disponibles.append(indice)
        if vecinas_disponibles != []:
            return random.choice(vecinas_disponibles)
        else:
            return None

def imprimir(matriz, snapshot, turno, muertes_conejos, muertes_zorros):
    """
    descripcion.
    args:
        matriz, snapshot
        turno
        muertes_conejos
        muertes_zorros
    returns:
        snapshot del turno impreso
        None, si se debe frenar la simulacion
    """
    
    cantidad_conejos = 0
    cantidad_zorros = 0
    cantidad_pasto = 0

    fila = 0
    columna = 1
    
    for celda in matriz:
        
        if celda[1] == 'pasto': # primero se analiza toda la matriz para ver las cantidades de zorros, conejos y pasto
            cantidad_pasto += 1
        elif celda[1] == None:
            pass
        elif celda[1]['tipo'] == 'conejo':
            cantidad_conejos += 1
        else:
            cantidad_zorros += 1

    
    for celda in matriz:
        
        if fila == (n // 4): # Cuando se haya impreso la cuarta parte de las filas, se imprime la informacion de conejos, zorros y pasto
            print('-' * n * 2)
            print (f'\nTurno: {turno}   🐇 Conejos: {cantidad_conejos}  🦊 Zorros: {cantidad_zorros}    🌳Pasto: {cantidad_pasto}')
            print('-' * n * 2)
            fila += 1

        if celda[1] == 'pasto': # Si es pasto, usa el atributo 'colored' de la libreria 'termcolor' para imprimir en color verde, lo mismo para los zorros y los conejos
            print(colored('▓▓', 'green'), end='')
        elif celda[1] == None:
            print('  ', end='')
        elif celda[1]['tipo'] == 'conejo':
            print(colored('▓▓', 'cyan'), end='')
        else:
            print(colored('▓▓', 'red'), end='')
           
        if columna == n:
            # Cuando llega al final de la fila imprime un string vacio sin end='' y el numero de la columna vuelve a ser 1.
            print('')
            columna = 1
            fila += 1
        else:
            columna += 1 # Si aun no llego al final de la fila, agrega una columna al indice

    snapshot = deepcopy(matriz)
    if cantidad_conejos != 0 and cantidad_zorros != 0:
        return snapshot
    else:
        return None

def __main__():
    matriz = comienzo()
    snapshot = deepcopy(matriz)
    muertes_conejos = []
    muertes_zorros = []

    
    for turno in range(tmax):
        time.sleep(0.5)
        os.system('cls')
        resultado_imprimir = imprimir(matriz, snapshot, (turno +1), muertes_conejos, muertes_zorros)
        if resultado_imprimir != None:
            snapshot = resultado_imprimir
        else:
            break
        
        # paso 1 y 2
        for celda in matriz: # 1. expansion de pasto y 2. decision de movimiento de los animales
            if celda[1] == 'pasto': # expansion del pasto
                celda_seleccionada = expansion_pasto(celda, snapshot)
                if celda_seleccionada != None:
                    matriz[celda_seleccionada][1] = 'pasto'
            
            elif str(type(celda[1])) == '<class \'dict\'>': # decision de movimiento de  cada animal
                indice = encontrar_indice(celda)
                movimiento_siguiente = decision_movimiento(celda, snapshot, muertes_conejos, muertes_zorros)
                if str(type(celda[1])) == '<class \'dict\'>':
                    matriz[indice][1]['movimiento'] = movimiento_siguiente
        
        # paso 3
        for celda in matriz: # 3. movimiento de los zorros
            indice = encontrar_indice(celda)
            if str(type(celda[1])) == '<class \'dict\'>':
                
                movimiento = celda[1]['movimiento']
                tiene_movimiento = (movimiento != None)
                es_zorro = (celda[1]['tipo'] == 'zorro')
                
                if tiene_movimiento == True:
                    destino_no_animal = (str(type(matriz[movimiento][1])) != '<class \'dict\'>')
                else:
                    destino_no_animal = False  
                
                if tiene_movimiento and es_zorro and destino_no_animal:
                            matriz[movimiento][1] = deepcopy(celda[1])
                            matriz[indice][1] = None
                            matriz[movimiento][1]['origen'] = indice
                else: 
                    matriz[indice][1]['origen'] = indice
        
        # paso 4                
        for celda in matriz: # 4. movimiento de los conejos
            indice = encontrar_indice(celda)
            
            es_animal = (str(type(celda[1])) == '<class \'dict\'>')
            
            
            if es_animal:
                es_conejo = (celda[1]['tipo'] == 'conejo')
                movimiento = celda[1]['movimiento']
                if movimiento != None and es_conejo:
                    matriz[indice][1]['origen'] = indice    
                    movimiento_no_animal = (str(type(matriz[movimiento][1])) != '<class \'dict\'>')
                    
                    if movimiento_no_animal == True:
                        era_pasto = (snapshot[movimiento][1] == 'pasto')
                        
                        matriz[movimiento][1] = deepcopy(celda[1])
                        matriz[indice][1] = None
                        matriz[movimiento][1]['origen'] = indice
                        
                        if era_pasto == True:
                            matriz[movimiento][1]['energia'] += gc # si era pasto, gana energia
                            
                    elif matriz[movimiento][1]['tipo'] == 'zorro':
                        muertes_conejos.append(celda[1]['edad'])
                        matriz[movimiento][1]['energia'] += gz
                        matriz[indice][1] = None
                        matriz[movimiento][1]['origen'] = indice
            
        # paso 5                
        for celda in matriz: # 5. reproduccion de los animales
            indice = encontrar_indice(celda)
            es_animal = (str(type(celda[1])) == '<class \'dict\'>')
            if es_animal == True:
                origen = celda[1]['origen']
                
                # condiciones para que se reproduzca el animal
                c1 = (matriz[origen][1] == None)
                c2 = (celda[1]['energia'] >= emin)
                cc = (random.random() < prc) # prob conejo
                cz = (random.random() < prz) # prob zorro
                
                if celda[1]['tipo'] == 'conejo' and  c1 and c2 and cc: 
                    matriz[origen][1] = {"tipo":    "conejo", 
                    "energia": ec,   # energía actual del animal 
                    "edad": 0,    # cantidad de turnos que lleva vivo
                    'origen': origen
                    }
                elif celda[1]['tipo'] == 'zorro' and c1 and c2 and cz: 
                    matriz[origen][1] = {"tipo": "zorro", 
                    "energia": ez,   # energía actual del animal 
                    "edad": 0,    # cantidad de turnos que lleva vivo
                    'origen': origen
                    }
    
if __name__ == '__main__':
    __main__()
                        
                
  