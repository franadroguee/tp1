import tp1_funciones_Adrogue as funciones
import os

total = {}
probabilidades = range (1, 40, 2)
repeticiones = 50
ejecuciones_totales = len(probabilidades) * repeticiones
carga = 0

for dz in probabilidades:
    dz /= 100
    ejecuciones_efectivas = 0
    for repeticion in range(repeticiones):
        carga += (100 / ejecuciones_totales)
        os.system('cls')
        print(f'{round(carga, 2)} %')
        print(total)
        efectividad = not funciones.ejercicio_3(25, 0.12, dz, 0.35, 5, 12, 4, 8, 0.5, 0.18, 0.18, 4, 200)
        if efectividad:
            ejecuciones_efectivas += 1
    
    total[dz] = f'{ejecuciones_efectivas * 100 / repeticiones} %'
    
print('+' + '-' * 10 + '+' + '-' * 20 + '+')
print('|' + '  dz      ' + '|' + '  Sin extinciones   ' + '|')
print('+' + '-' * 10 + '+' + '-' * 20 + '+')

for key in total:
    print (f'|  {key}    |    {total[key]}            |')
    print('+' + '-' * 10 + '+' + '-' * 20 + '+')
