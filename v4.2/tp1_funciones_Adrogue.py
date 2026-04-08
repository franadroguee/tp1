from termcolor import colored
import random
import time
import os
from copy import deepcopy

def encontrar_indice(celda, n):
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

def encontrar_vecinas(celda, n):
    """
    descripcion.
    args:
        celda
    returns:
        celdas_vecinas ([x, y])
    """
    
    x = celda[0][0]
    y = celda[0][1]
    vecinas = [] # Vacia la lista
        
    if (x-1) >= 0: # Controla que la celda no este fuera de la grilla
        vecina = ([x-1, y])
        vecinas.append(vecina) # Agrega la celda a la lista, ya que se comprobo que esta dentro de la cuadrilla
            
    if (y-1) >= 0: # Controla que la celda no este fuera de la grilla
        vecina = ([x, y-1])
        vecinas.append(vecina)
        
    if (x+1) < n: # Controla que la celda no este fuera de la grilla
        vecina = ([x+1, y])
        vecinas.append(vecina)
        
    if (y+1) < n: # Controla que la celda no este fuera de la grilla
        vecina = ([x, y+1])
        vecinas.append(vecina)
        
    return vecinas # Devuelve la lista de matriz vecinas a donde haya sido llamada la funcion

def comienzo(n, dp, dc, dz, ec, ez):
    """
    Descripcion.
    Args:
        None
    Returns:
        matriz
    """
    matriz = []
    
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
    
def expansion_pasto(celda, snapshot, pp, n):
    """
    descripcion.
    args:
        celda de pasto
        snapshot
    returns:
        indice celda donde crecera pasto
    """
    vecinas = encontrar_vecinas(celda, n)
    vecinas_disponibles = []
    for vecina in vecinas:
        indice = encontrar_indice(vecina, n)
        if snapshot[indice][1] == None:
            vecinas_disponibles.append(indice)
            
    if vecinas_disponibles != [] and random.random() < pp:
        return random.choice(vecinas_disponibles)
    else:
        return None

def decision_movimiento(matriz, celda, snapshot, muertes_conejos, muertes_zorros, n):
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
            indice = encontrar_indice(celda, n)
            muertes_zorros.append(celda[1]['edad'])
            matriz[indice][1] = None
            return None

        vecinas = encontrar_vecinas(celda, n)
        vecinas_disponibles = []
        for vecina in vecinas:
            indice = encontrar_indice(vecina, n)
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
            indice = encontrar_indice(celda, n)
            muertes_conejos.append(celda[1]['edad'])
            matriz[indice][1] = None
            return None

        vecinas = encontrar_vecinas(celda, n)
        vecinas_disponibles = []
        for vecina in vecinas:
            indice = encontrar_indice(vecina, n)
            if snapshot[indice][1] == 'pasto' or snapshot[indice][1] == None:
                vecinas_disponibles.append(indice)
            elif snapshot[indice][1]['tipo'] == 'zorro':
                vecinas_disponibles.append(indice)
        if vecinas_disponibles != []:
            return random.choice(vecinas_disponibles)
        else:
            return None

def contar(matriz):
    """
    descripcion.
    args:
        matriz
    returns:
        cantidad_conejos, cantidad_zorros
    """
    
    cantidad_conejos = 0
    cantidad_zorros = 0
    
    for celda in matriz:
        
        if celda[1] == 'pasto' or celda[1] == None:
            pass
        elif celda[1]['tipo'] == 'conejo':
            cantidad_conejos += 1
        else:
            cantidad_zorros += 1
            
    return (cantidad_conejos, cantidad_zorros)            

def imprimir(matriz, n, turno, cantidad_conejos, cantidad_zorros):
    """
    descripcion.
    args:
        matriz, snapshot
        turno
        muertes_conejos
        muertes_zorros
    returns:
        si se debe continuar, True
        si no, False
    """
    
    fila = 0
    columna = 1
    

    
    for celda in matriz:
        
        if fila == (n // 4): # Cuando se haya impreso la cuarta parte de las filas, se imprime la informacion de conejos, zorros y pasto
            print('-' * n * 2)
            print (f'\nTurno: {turno}   🐇 Conejos: {cantidad_conejos}  🦊 Zorros: {cantidad_zorros}')
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

def reescribir_snapshot(matriz):
    snapshot = deepcopy(matriz)
    return snapshot

def paso_1_2(matriz, snapshot, muertes_conejos, muertes_zorros, n, pp):
    for celda in matriz: # 1. expansion de pasto y 2. decision de movimiento de los animales
        if celda[1] == 'pasto': # expansion del pasto
            celda_seleccionada = expansion_pasto(celda, snapshot, pp, n)
            if celda_seleccionada != None:
                matriz[celda_seleccionada][1] = 'pasto'
        
        elif str(type(celda[1])) == '<class \'dict\'>': # decision de movimiento de  cada animal
            indice = encontrar_indice(celda, n)
            movimiento_siguiente = decision_movimiento(matriz, celda, snapshot, muertes_conejos, muertes_zorros, n)
            if str(type(celda[1])) == '<class \'dict\'>':
                matriz[indice][1]['movimiento'] = movimiento_siguiente

def paso_3(matriz, n):
    for celda in matriz: # 3. movimiento de los zorros
        indice = encontrar_indice(celda, n)
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

def paso_4(matriz, snapshot, gc, gz, n):
    for celda in matriz: # 4. movimiento de los conejos
        indice = encontrar_indice(celda, n)
        
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
                    matriz[movimiento][1]['energia'] += gz
                    matriz[indice][1] = None
                    matriz[movimiento][1]['origen'] = indice

def paso_5(matriz, ec, ez, prc, prz, emin, n):
    for celda in matriz: # 5. reproduccion de los animales
        indice = encontrar_indice(celda, n)
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

def pasos(matriz, snapshot, n, ec, ez, gc, gz, pp, prc, prz, emin, muertes_conejos, muertes_zorros):
    """
    descripcion.
    args:
        matriz, 
        snapshot, 
        n, ec, ez, gc, gz, pp, prc, prz, emin, muertes_conejos, muertes_zorros
    returns:
        muertes_conejos
        muertes_zorros
    """
    
    # paso 1 y 2
    paso_1_2(matriz, snapshot, muertes_conejos, muertes_zorros, n, pp)
    # paso 3
    paso_3(matriz, n)
    # paso 4                
    paso_4(matriz, snapshot, gc, gz, n)
    # paso 5 
    paso_5(matriz, ec, ez, prc, prz, emin, n)
    
    return muertes_conejos, muertes_zorros                                       

def ejercicio_1(n, dc, dz, dp, ec, ez, gc, gz, pp, prc, prz, emin, tmax):

    """
    desctipcion.
    args: 
        n = int: tamaño de la grilla

        dc = float: densidad inicial de conejos. Probabilidad de que una celda empiece con un conejo.
        dz = float: densidad inicial de zorros. Probabilidad de que una celda empiece con un zorro.
        dp = float: densidad inicial de pasto. Probabilidad de que una celda vacía (sin animal) empiece con pasto.

        ec = int: energía inicial de los conejos y de cada conejo recién nacido.
        ez = int: energía inicial de los zorros y de cada zorro recién nacido.

        gc = int: energía que gana un conejo al comer pasto.
        gz = int: energía que gana un zorro al comer un conejo.

        pp = int: probabilidad de que en un turno dado el pasto crezca en una celda vacía adyacente.
        prc =int: probabilidad de que un conejo se reproduzca en un turno dado (si tiene energía suficiente).
        prz =int: probabilidad de que un zorro se reproduzca en un turno dado (si tiene energía suficiente).

        emin = int: energía mínima necesaria para que un animal pueda reproducirse.
        tmax = int: turnos
    returns:
        None
    """

    matriz = comienzo(n, dp, dc, dz, ec, ez)
    snapshot = deepcopy(matriz)
    muertes_conejos = []
    muertes_zorros = []
    
    for turno in range(tmax):
        time.sleep(0.1)
        os.system('cls')
        cantidad_conejos, cantidad_zorros = contar(matriz)
        
        if cantidad_conejos != 0 and cantidad_zorros != 0:
            pass
        else: # si hay alguna extinicon, imprime una ultima vez y rompe el ciclo
            imprimir(matriz, n, (turno +1), cantidad_conejos, cantidad_zorros)
            break
        
        imprimir(matriz, n, (turno +1), cantidad_conejos, cantidad_zorros)
        
        snapshot = reescribir_snapshot(matriz)
        
        pasos(matriz, snapshot, n, ec, ez, gc, gz, pp, prc, prz, emin, muertes_conejos, muertes_zorros)
  
def ejercicio_2(n, dc, dz, dp, ec, ez, gc, gz, pp, prc, prz, emin, tmax):
    
    """
    desctipcion.
    args: 
        n = int: tamaño de la grilla

        dc = float: densidad inicial de conejos. Probabilidad de que una celda empiece con un conejo.
        dz = float: densidad inicial de zorros. Probabilidad de que una celda empiece con un zorro.
        dp = float: densidad inicial de pasto. Probabilidad de que una celda vacía (sin animal) empiece con pasto.

        ec = int: energía inicial de los conejos y de cada conejo recién nacido.
        ez = int: energía inicial de los zorros y de cada zorro recién nacido.

        gc = int: energía que gana un conejo al comer pasto.
        gz = int: energía que gana un zorro al comer un conejo.

        pp = int: probabilidad de que en un turno dado el pasto crezca en una celda vacía adyacente.
        prc =int: probabilidad de que un conejo se reproduzca en un turno dado (si tiene energía suficiente).
        prz =int: probabilidad de que un zorro se reproduzca en un turno dado (si tiene energía suficiente).

        emin = int: energía mínima necesaria para que un animal pueda reproducirse.
        tmax = int: turnos
    returns:
        muertes_conejos, muertes_zorros
    """

    matriz = comienzo(n, dp, dc, dz, ec, ez)
    snapshot = deepcopy(matriz)
    muertes_conejos = []
    muertes_zorros = []
    
    for turno in range(tmax):
        cantidad_conejos, cantidad_zorros = contar(matriz)
        
        if cantidad_conejos != 0 and cantidad_zorros != 0:
            pass
        else:
            break
                
        snapshot = reescribir_snapshot(matriz)
        
        muertes_conejos, muertes_zorros = pasos(matriz, snapshot, n, ec, ez, gc, gz, pp, prc, prz, emin, muertes_conejos, muertes_zorros)
        
    return muertes_conejos, muertes_zorros

def ejercicio_3(n, dc, dz, dp, ec, ez, gc, gz, pp, prc, prz, emin, tmax):
    
    """
    desctipcion.
    args: 
        n = int: tamaño de la grilla

        dc = float: densidad inicial de conejos. Probabilidad de que una celda empiece con un conejo.
        dz = float: densidad inicial de zorros. Probabilidad de que una celda empiece con un zorro.
        dp = float: densidad inicial de pasto. Probabilidad de que una celda vacía (sin animal) empiece con pasto.

        ec = int: energía inicial de los conejos y de cada conejo recién nacido.
        ez = int: energía inicial de los zorros y de cada zorro recién nacido.

        gc = int: energía que gana un conejo al comer pasto.
        gz = int: energía que gana un zorro al comer un conejo.

        pp = int: probabilidad de que en un turno dado el pasto crezca en una celda vacía adyacente.
        prc =int: probabilidad de que un conejo se reproduzca en un turno dado (si tiene energía suficiente).
        prz =int: probabilidad de que un zorro se reproduzca en un turno dado (si tiene energía suficiente).

        emin = int: energía mínima necesaria para que un animal pueda reproducirse.
        tmax = int: turnos
    returns:
        True si hubo alguna extincion
        False si se completaron todos los turnos sin ninguna extincion
    """

    matriz = comienzo(n, dp, dc, dz, ec, ez)
    snapshot = deepcopy(matriz)
    muertes_conejos = []
    muertes_zorros = []
    
    for turno in range(tmax):
        cantidad_conejos, cantidad_zorros = contar(matriz)
           
        if cantidad_conejos != 0 and cantidad_zorros != 0:
            extincion = False
        else:
            extincion = True
            break
        
                
        snapshot = reescribir_snapshot(matriz)
        
        pasos(matriz, snapshot, n, ec, ez, gc, gz, pp, prc, prz, emin, muertes_conejos, muertes_zorros)
        
    return extincion

def ejercicio_3_2(n, dc, dz, dp, ec, ez, gc, gz, pp, prc, prz, emin, tmax):
    
    """
    desctipcion.
    args: 
        n = int: tamaño de la grilla

        dc = float: densidad inicial de conejos. Probabilidad de que una celda empiece con un conejo.
        dz = float: densidad inicial de zorros. Probabilidad de que una celda empiece con un zorro.
        dp = float: densidad inicial de pasto. Probabilidad de que una celda vacía (sin animal) empiece con pasto.

        ec = int: energía inicial de los conejos y de cada conejo recién nacido.
        ez = int: energía inicial de los zorros y de cada zorro recién nacido.

        gc = int: energía que gana un conejo al comer pasto.
        gz = int: energía que gana un zorro al comer un conejo.

        pp = int: probabilidad de que en un turno dado el pasto crezca en una celda vacía adyacente.
        prc =int: probabilidad de que un conejo se reproduzca en un turno dado (si tiene energía suficiente).
        prz =int: probabilidad de que un zorro se reproduzca en un turno dado (si tiene energía suficiente).

        emin = int: energía mínima necesaria para que un animal pueda reproducirse.
        tmax = int: turnos
    """

    matriz = comienzo(n, dp, dc, dz, ec, ez)
    snapshot = deepcopy(matriz)
    muertes_conejos = []
    muertes_zorros = []
    
    for turno in range(tmax):
        cantidad_conejos, cantidad_zorros = contar(matriz)
        
        if cantidad_conejos != 0 and cantidad_zorros != 0:
            extincion = False
        else:
            if cantidad_conejos == 0:
                extincion = True
            else:
                extincion == False
            break
        
                
        snapshot = reescribir_snapshot(matriz)
        
        pasos(matriz, snapshot, n, ec, ez, gc, gz, pp, prc, prz, emin, muertes_conejos, muertes_zorros)
        
    return extincion

