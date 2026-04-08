from termcolor import colored
import random
import time
import os

"""
VARIABLES FIJAS DE LA SIMULACION
"""
snapshot = [] ###La lista que contendra la informacion de cada celda. Cada item de la lista sera a su vez una lista, donde el primer item (0) sea su posicion y el segundo sea su tipo.
matriz = []

muertes_conejos = []
muertes_zorros = []

n = 20 ###tamaño de la grilla

dc = 0.1 ###densidad inicial de conejos. Probabilidad de que una celda empiece con un conejo.
dz = 0. ###densidad inicial de zorros. Probabilidad de que una celda empiece con un zorro.
dp = 0.8 ###densidad inicial de pasto. Probabilidad de que una celda vacía (sin animal) empiece con pasto.

ec = 10 ###energía inicial de los conejos y de cada conejo recién nacido.
ez = 12 ###energía inicial de los zorros y de cada zorro recién nacido.

gc = 1000 ###energía que gana un conejo al comer pasto.
gz = 8 ###energía que gana un zorro al comer un conejo.

pp = 0.5 ###probabilidad de que en un turno dado el pasto crezca en una celda vacía adyacente.
prc = 0.18 ###probabilidad de que un conejo se reproduzca en un turno dado (si tiene energía suficiente).
prz = 0.18 ###probabilidad de que un zorro se reproduzca en un turno dado (si tiene energía suficiente).

emin = 4 ###energía mínima necesaria para que un animal pueda reproducirse.
tmax = 200 

def encontrar_indice(celda):
    cordenadas = celda
    numero = int(cordenadas[0]) + (int(cordenadas[1]) * n)
    return numero

def encontrar_vecinas(celda):
    ###Las matrizs vecinas sseran de la forma x +- 1, y +- 1
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
                snapshot.append([[columna, fila], {
                    "tipo":    "conejo",
                    "energia": ec,   # energía actual del animal
                    "edad": 0    # cantidad de turnos que lleva vivo
                }])
            elif probabilidad < (dc + dz):
                snapshot.append([[columna, fila], {
                    "tipo":    "zorro",
                    "energia": ez,   # energía actual del animal
                    "edad": 0    # cantidad de turnos que lleva vivo
                }])
            elif probabilidad < (dc + dz + dp):
                snapshot.append([[columna, fila], 'pasto'])
            else:
                snapshot.append([[columna, fila],'None'])
    
    for item in range(len(snapshot)):
        matriz.append(list(snapshot)[item])
    
def imprimir(turno):
    cantidad_conejos = 0
    cantidad_zorros = 0
    cantidad_pasto = 0

    columna = 1
    for celda in matriz:
        if celda[1] == 'pasto': #Si es pasto, usa el atributo 'colored' de la libreria 'termcolor' para imprimir en color verde, lo mismo para los zorros y los conejos
            print(colored('▓▓', 'green'), end='')
            cantidad_pasto += 1
        elif celda[1] == 'None':
            print('  ', end='')
        elif celda[1]['tipo'] == 'conejo':
            print(colored('▓▓', 'cyan'), end='')
            cantidad_conejos += 1
        else:
            print(colored('▓▓', 'red'), end='')
            cantidad_zorros += 1

        if columna == n:
            #Cuando llega al final de la fila imprime un string vacio sin end='' y el numero de la columna vuelve a ser 1.
            print('')
            columna = 1
        else:
            columna += 1 #Si aun no llego al final de la fila, agrega una columna al indice
    
    for item in range(len(matriz)):
        snapshot[item] = list(matriz)[item]
    print (f'\nTurno: {turno}   🐇 Conejos: {cantidad_conejos}  🦊 Zorros: {cantidad_zorros}    Cantidad de pasto: {cantidad_pasto}.')
            
def expansion_pasto(celda):
    vecinas_disponibles = []
    vecinas = encontrar_vecinas(celda) #Devuelve una lista con las matriz vecinas a la celda analizada
    for vecina in vecinas:
        #Analiza cada celda vecina por separado para verificar que este disponible. De estarlo, la agrega a la lista 'vecinas_disponibles'
        numero = encontrar_indice(vecina)
        if snapshot[numero][1] == 'None':
            vecinas_disponibles.append(numero)
        
    if vecinas_disponibles != [] and random.random() < pp: #Si la lista de vecinas disponibles no esta vacia, hace el calculo estadistico
        eleccion = random.choice(vecinas_disponibles)  
        matriz[eleccion] = [matriz[eleccion][0], 'pasto']
    
def decision_movimiento(celda):
    vecinas_disponibles = []
    muerto = False
    animal = encontrar_indice(celda[0])
    vecinas = encontrar_vecinas(celda) #Devuelve una lista con las matriz vecinas a la celda analizada
    celda[1]['edad'] += 1
    if celda[1]['tipo'] == 'conejo': #Determina si la celda que esta ciendo analizada es un zorro o un conejo
        #Si es un conejo, pierde 1 de energia y puede moverse a una celda que contenga pasto en el snapshot
        celda[1]['energia'] -= 1 
        if celda[1]['energia'] <= 0:
            matriz[animal][1] = 'None'
            muerto = True
        else:
            for vecina in vecinas: #Analiza cada celda vecina por separado para verificar que este disponible. De estarlo, la agrega a la lista 'vecinas_disponibles'
                numero = encontrar_indice(vecina)
                if snapshot[numero][1] == 'None':
                    vecinas_disponibles.append(numero)
                elif snapshot[numero][1] == 'pasto':
                    vecinas_disponibles.append(numero)
    elif celda[1]['tipo'] == 'zorro':
        #Si es un zorro, pierde dos puntos de energia pero puede moverse a una celda que tenga un conejo en el snapshot
        celda[1]['energia'] -= 2 
        if celda[1]['energia'] <= 0:
            matriz[animal][1] = 'None'
            muerto = True
        else:
            for vecina in vecinas: #Analiza cada celda vecina por separado para verificar que este disponible. De estarlo, la agrega a la lista 'vecinas_disponibles'
                numero = encontrar_indice(vecina)
                if snapshot[numero][1] == 'None':
                    vecinas_disponibles.append(numero)
                elif snapshot[numero][1] == 'pasto':
                    vecinas_disponibles.append(numero)
                elif snapshot[numero][1]['tipo'] == 'conejo':
                    vecinas_disponibles.append(numero)
    if muerto == False:
        if vecinas_disponibles != []:
            celda[1]['movimiento'] = random.choice(vecinas_disponibles)
        else:
            celda[1]['movimiento'] = ''
                
def movimiento_zorro(celda):
    numero = celda[1]['movimiento']
    zorro = encontrar_indice(celda[0])
    if matriz[numero][1] == 'pasto' or matriz[numero][1] == 'None':
        matriz[numero][1] = celda[1]
        matriz[zorro][1] = 'None'
    elif matriz[numero][1]['tipo'] == 'conejo':
        matriz[numero][1] = celda[1]
        matriz[zorro][1] = 'None'
        
def movimiento_conejo(celda):
    numero = celda[1]['movimiento']
    conejo = encontrar_indice(celda[0])
    if matriz[numero][1] == 'pasto' or matriz[numero][1] == 'None':
        matriz[numero][1] = celda[1]
        matriz[conejo][1] = 'None'
        if snapshot[numero][1] == 'pasto':
            matriz[numero][1]['energia'] += gc

    elif matriz[numero][1]['tipo'] == 'zorro':
        muertes_conejos.append(matriz[conejo][1]['edad'])
        matriz[conejo][1] = 'None'
        matriz[numero][1]['energia'] += gz

###----------------------------------------------------------------###

def __main__():
    comienzo()
    for turno in range(tmax):
        time.sleep(0.3)
        os.system('cls')
        imprimir(turno)
        for celda in matriz:
            #Primero se expande el pasto y los animales deciden su proximo movimiento
            if celda[1] == 'pasto':
                expansion_pasto(celda)
            elif celda[1] == 'None': #Se deben descartar las matriz de tipo 'None' ya que si se intenta buscar su valor 'tipo' como si fuese un diccionario, ocurre un error
                pass
            elif celda[1]['tipo'] == 'conejo' or celda[1]['tipo'] == 'zorro':
                decision_movimiento(celda)
            
        for celda in matriz: #Luego de eso, efectivamente se mueven los animales
            if celda[1] == 'pasto' or celda[1] == 'None':
                pass
            elif celda[1]['tipo'] == 'zorro' and celda[1]['movimiento'] != '':
                movimiento_zorro(celda)
            
        for celda in matriz: #Luego de eso, efectivamente se mueven los animales
            if celda[1] == 'pasto' or celda[1] == 'None':
                pass
            elif celda[1]['tipo'] == 'conejo' and celda[1]['movimiento'] != '':
                movimiento_conejo(celda)
__main__()
