
Sistema de Gestión de Países

Trabajo Práctico Integrador – Programación 1  
Institución: [Universidad Tecnológica Nacional] 
Carrera: [Programación]  
Materia: Programación 1  
Fecha de entrega: [29/06/2026]



Descripción del programa

Este sistema permite gestionar información de países a través de una aplicación de consola desarrollada en Python. El programa lee datos desde un archivo CSV, los almacena en memoria mediante listas de diccionarios, y ofrece un menú interactivo para realizar operaciones como:

- Agregar nuevos países.
- Actualizar población y superficie de países existentes.
- Buscar países por nombre (coincidencia parcial o exacta).
- Filtrar países por continente, rango de población o rango de superficie.
- Ordenar países por nombre, población o superficie (ascendente/descendente).
- Mostrar estadísticas clave (país con mayor/menor población, promedios, cantidad de países por continente).

El proyecto fue desarrollado como parte del Trabajo Práctico Integrador de la materia Programación 1, con el objetivo de afianzar conceptos de estructuras de datos, modularización, manejo de archivos y algoritmos de ordenamiento/filtrado.


Instrucciones de uso

Requisitos previos

- Python 3.x instalado en tu sistema.
- Git(opcional, para clonar el repositorio).
Clonar el repositorio

```bash
git clone https://github.com/Namyiokai/UTN_TPI_Prog1.git
cd UTN_TPI_Prog1

#al ejecutar el programa se muestra: 

Sistema de gestión de países
1. Agregar país
2. Actualizar país
3. Buscar país por nombre
4. Filtrar países
5. Ordenar países
6. Estadísticas
7. Guardar y salir

Seleccione una opción (1-7): 1
Agregar nuevo país
Ingrese el nombre del país: Chile
Ingrese la población (número entero): 19600000
Ingrese la superficie en km² (número entero): 756102
Ingrese el continente: América

salida: 
País 'Chile' agregado correctamente.
Datos guardados exitosamente en /content/data/paises.csv (18 países)

