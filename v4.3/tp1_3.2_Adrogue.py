import tp1_funciones_Adrogue as funciones
import os

"""
como los porcentajes que me devolvian las simulaciones en el ejercicio 3 estaban muy alejadas 
de los porcentajes demostrativos del pdf explicativo, hice esta version, la 3.2 
en la que incluye como ejecuciones efectivas aquellas en las que ninguna especie se haya extinto o solo los zorros lo hayan hecho 
(a diferencia de la otra que solo tomaba en cuenta los casos en los que ambas especies llegaban al final de Tmax con vida). 
"""

total = {}
probabilidades = range (1, 40, 2) # se toman los numeros entre el 1 y el 40 en saltos de dos y luego se los divide por 100
repeticiones = 50
ejecuciones_totales = len(probabilidades) * repeticiones
porcentaje = 0

for dz in probabilidades:
    dz /= 100
    ejecuciones_efectivas = 0
    for repeticion in range(repeticiones):
        porcentaje += (100 / ejecuciones_totales)
        os.system('cls')
        print(f'{round(porcentaje, 2)} %')
        print(total)
        efectividad = not funciones.ejercicio_3_2(25, 0.12, dz, 0.35, 5, 12, 4, 8, 0.5, 0.18, 0.18, 4, 200)
        if efectividad:
            ejecuciones_efectivas += 1
    
    total[dz] = f'{ejecuciones_efectivas * 2} %'
    
print('+' + '-' * 10 + '+' + '-' * 20 + '+')
print('|' + '  dz      ' + '|' + '  Sin extinciones   ' + '|')
print('+' + '-' * 10 + '+' + '-' * 20 + '+')

for key in total:
    print (f'|  {key}    |    {total[key]}            |')
    print('+' + '-' * 10 + '+' + '-' * 20 + '+')
