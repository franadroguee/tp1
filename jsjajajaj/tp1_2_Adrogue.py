import tp1_funciones_Adrogue as funciones
import os

muertes_conejos_t = []
muertes_zorros_t = []

repeticiones = 100

for repeticion in range(repeticiones):
    os.system('cls')
    print(f'{repeticion * 100 / repeticiones}%')
    
    muertes_conejos, muertes_zorros = funciones.ejercicio_2(50, 0.12, 0.2, 0.35, 5, 12, 4, 8, 0.5, 0.18, 0.18, 4, 200)
    
    for item in muertes_conejos:
        muertes_conejos_t.append(item)
    for item in muertes_zorros:
        muertes_zorros_t.append(item)

os.system('cls')
print(f'Muertes registradas: Conejos: {len(muertes_conejos_t)} | Zorros: {len(muertes_zorros_t)}')
print(f'Esperanza de vida del conejo: {round((sum(muertes_conejos_t)/len(muertes_conejos_t)), 2)}')
print(f'Esperanza de vida del zorro: {round((sum(muertes_zorros_t)/len(muertes_zorros_t)), 2)}')

