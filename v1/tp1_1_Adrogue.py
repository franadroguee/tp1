from tp1_funciones_Adrogue import comienzo, imprimir, expansion_pasto, movimiento_zorro, movimiento_conejo, matriz
import os
import time

comienzo ()

while True:
    os.system('cls')
    imprimir()
    for celda in matriz:
        if matriz[celda] == 'pasto':
            expansion_pasto(celda)
        elif matriz[celda] == 'None':
            pass
        elif matriz[celda]['tipo'] == 'conejo':
            movimiento_conejo(celda)
        elif matriz[celda]['tipo'] == 'zorro':
            movimiento_zorro(celda)

    time.sleep(0.3)