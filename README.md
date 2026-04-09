# INFO
El siguiente repositorio contiene una simulacion de una grilla de tamaño n x n en la cual cada celda puede ser un pasto, un conejo, un zorro o estar vacia. 

las celdas de pasto se expanden a sus celdas vecinas con probabilidad pp
los conejos se comen el pasto si se mueven a una celda con esto
los zorros se comen los conejos si el conejo se mueve a una celda con un zorro

los zorros ganan gz energia cuando comen un conejo
los  conejos ganan gc energia cuando comen pasto

# EJERCICIOS
el ejercicio 1 imprime una simulacion en la terminal, (los zorros son rojos, los conejos azules y los pastos verdes) 
en una matriz de 25 x 25 con un largo maximo de 200 turnos (con posibilidad de terminar antes si alguna especie se extingue)

el ejercicio 2 ejecuta 100 simulaciones de estas (sin imprimir) y calcula la esperanza de vida de los conejos y los zorros
ademas de la cantidad total de muertes de cada uno a lo largo de las 100 simulaciones.

el ejercicio 3 ejecuta un total de 1000 simulaciones (primero con una densidad inicial de zorros de 0.01 (1%), luego 0.03 y asi
en saltos de 0.02 hasta llegar una densidad inicial de zorros de 0.39.
por cada densidad, ejecuta 50 simulaciones 

# ADVERTENCIA

Las funciones se llaman constantemente con todos los parametros de la simulacion 
(los que sean relevantes a la funcion llamada)

Esto es así para que no sean variables globales sino que sean locales 
dentro de las funciones en las que se ejecutan y asi poder alterar los parametros 
cada vez que se ejecuta una simulacion.

# FUENTES

Todos los codigos del repositorio se hicieron en conformidad con las instrucciones en tp1.pdf.


## PDF
[tp1.pdf](https://github.com/user-attachments/files/26606465/tp1.pdf)
