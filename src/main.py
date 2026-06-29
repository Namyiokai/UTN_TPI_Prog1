
import sys
import os

# Agregar la carpeta src al path para importar módulos
sys.path.append('/content/UTN_TPI_Prog1/src')

from funciones_csv import cargar_datos, guardar_datos
from utilidades import (
    validar_entero_positivo,
    validar_texto_no_vacio,
    buscar_pais_por_nombre,
    mostrar_lista_paises,
    mostrar_pais,
    obtener_continentes_unicos,
    mostrar_continentes_disponibles,
    solicitar_entero,
    solicitar_texto,
    elegir_opcion
)

# Ruta del archivo CSV (se puede modificar según necesidad)
RUTA_CSV = 'data/paises.csv'

# Variable global para almacenar los datos en memoria
paises = []


def inicializar_datos():
  #Carga los datos desde el CSV al inicio del programa.
    global paises
    paises = cargar_datos(RUTA_CSV)
    if not paises:
        print("No se cargaron datos. Asegúrese de que el archivo CSV exista y tenga datos válidos.")
    return paises


def guardar_y_salir():
  #Guarda los datos y termina el programa.
    global paises
    print("Se guardaron los datos.")
    if guardar_datos(RUTA_CSV, paises):
        print("Datos guardados correctamente.")
    else:
        print("Error al guardar los datos.")
    print("Adios.")
    sys.exit(0)


# Funcionalidades del menú

def opcion_agregar_pais():
#Agrega un nuevo país con validación de campos."""
    global paises
    print("Agregar nuevo país")

    # Solicitar y validar nombre
    nombre_valido, nombre = validar_texto_no_vacio(input("Ingrese el nombre del país: "))
    if not nombre_valido:
        print(f"Error: {nombre}")
        return

    # Solicitar y validar población
    poblacion_valida, poblacion = validar_entero_positivo(input("Ingrese la población (número entero): "))
    if not poblacion_valida:
        print(f"Error: {poblacion}")
        return

    # Solicitar y validar superficie
    superficie_valida, superficie = validar_entero_positivo(input("Ingrese la superficie en km² (número entero): "))
    if not superficie_valida:
        print(f"Error: {superficie}")
        return

    # Solicitar y validar continente
    continente_valido, continente = validar_texto_no_vacio(input("Ingrese el continente: "))
    if not continente_valido:
        print(f"Error: {continente}")
        return

    # Crear el nuevo país
    nuevo_pais = {
        'nombre': nombre,
        'poblacion': poblacion,
        'superficie': superficie,
        'continente': continente
    }

    # Verificar si ya existe un país con el mismo nombre
    existente = [p for p in paises if p['nombre'].lower() == nombre.lower()]
    if existente:
        print(f"Ya existe un país con el nombre '{nombre}'. No se agregó.")
        return

    # Agregar a la lista
    paises.append(nuevo_pais)
    print(f"País '{nombre}' agregado correctamente.")

    # Guardar automáticamente después de agregar
    guardar_datos(RUTA_CSV, paises)


def opcion_actualizar_pais():
    #Actualiza la población y/o superficie de un país existente.
    global paises
    print("Actualizar país")

    if not paises:
        print("No hay países cargados.")
        return

    nombre_buscar = solicitar_texto("Ingrese el nombre del país a actualizar: ")
    resultados = buscar_pais_por_nombre(paises, nombre_buscar)

    if not resultados:
        print(f"No se encontraron países con '{nombre_buscar}'.")
        return

    if len(resultados) > 1:
        print(f"Se encontraron {len(resultados)} países con coincidencia:")
        mostrar_lista_paises(resultados, "Seleccione el país a actualizar")

        # Pedir que elija uno por índice (1..N)
        while True:
            try:
                seleccion = int(input("Ingrese el número del país a actualizar (0 para cancelar): "))
                if seleccion == 0:
                    print("Operación cancelada.")
                    return
                if 1 <= seleccion <= len(resultados):
                    pais_a_actualizar = resultados[seleccion - 1]
                    break
                else:
                    print(f"Número inválido. Debe ser entre 1 y {len(resultados)}.")
            except ValueError:
                print("Debe ingresar un número entero.")
    else:
        pais_a_actualizar = resultados[0]
        print(f"País encontrado:")
        mostrar_pais(pais_a_actualizar)

    # Ahora pedir qué actualizar
    print("\n¿Qué desea actualizar?")
    opciones = {
        '1': 'Población',
        '2': 'Superficie',
        '3': 'Ambos',
        '4': 'Cancelar'
    }
    eleccion = elegir_opcion("Seleccione una opción:", opciones)

    if eleccion == '4':
        print("Operación cancelada.")
        return

    # Actualizar según la opción
    if eleccion in ['1', '3']:
        # Nueva población
        while True:
            nueva_poblacion = input(f"Nueva población (actual: {pais_a_actualizar['poblacion']}): ")
            valido, valor = validar_entero_positivo(nueva_poblacion)
            if valido:
                pais_a_actualizar['poblacion'] = valor
                break
            else:
                print(f"{valor}")

    if eleccion in ['2', '3']:
        # Nueva superficie
        while True:
            nueva_superficie = input(f"Nueva superficie en km² (actual: {pais_a_actualizar['superficie']}): ")
            valido, valor = validar_entero_positivo(nueva_superficie)
            if valido:
                pais_a_actualizar['superficie'] = valor
                break
            else:
                print(f"{valor}")

    print(f"País '{pais_a_actualizar['nombre']}' actualizado correctamente.")
    mostrar_pais(pais_a_actualizar)

    # Guardar cambios
    guardar_datos(RUTA_CSV, paises)


def opcion_buscar_pais():
    #Busca países por nombre
    global paises
    print("Buscar país")

    if not paises:
        print("No hay países cargados.")
        return

    texto = solicitar_texto("Ingrese el nombre o parte del nombre a buscar: ")
    resultados = buscar_pais_por_nombre(paises, texto)

    if resultados:
        mostrar_lista_paises(resultados, f"Resultados para '{texto}'")
    else:
        print(f"No se encontraron países que contengan '{texto}'.")


def opcion_filtrar_por_continente():
  #Filtra países por continente.
    global paises
    print("Filtrar por continente")

    if not paises:
        print("No hay países cargados.")
        return

    # Mostrar continentes disponibles
    if not mostrar_continentes_disponibles(paises):
        return

    continente = solicitar_texto("Ingrese el nombre del continente a filtrar: ")

    # Buscar coincidencia exacta (sin distinguir mayúsculas)
    resultados = [p for p in paises if p['continente'].lower() == continente.lower()]

    if resultados:
        mostrar_lista_paises(resultados, f"Países en '{continente}'")
    else:
        print(f"No se encontraron países en el continente '{continente}'.")



def opcion_filtrar_por_poblacion():
    #Filtra países por rango de población.
    global paises
    print("Filtrar por rango de población")

    if not paises:
        print("No hay países cargados.")
        return

    # Solicitar mínimo
    min_str = input("Población mínima (presione Enter para omitir): ")
    min_pob = None
    if min_str.strip():
        valido, valor = validar_entero_positivo(min_str)
        if valido:
            min_pob = valor
        else:
            print(f"Error en mínimo: {valor}")
            return

    # Solicitar máximo
    max_str = input("Población máxima (presione Enter para omitir): ")
    max_pob = None
    if max_str.strip():
        valido, valor = validar_entero_positivo(max_str)
        if valido:
            max_pob = valor
        else:
            print(f"Error en máximo: {valor}")
            return

    # Verificar que mínimo <= máximo
    if min_pob is not None and max_pob is not None and min_pob > max_pob:
        print("Error: La población mínima no puede ser mayor que la máxima.")
        return

    # Filtrar
    resultados = []
    for p in paises:
        cumple = True
        if min_pob is not None and p['poblacion'] < min_pob:
            cumple = False
        if max_pob is not None and p['poblacion'] > max_pob:
            cumple = False
        if cumple:
            resultados.append(p)

    if resultados:
        rango_str = ""
        if min_pob is not None and max_pob is not None:
            rango_str = f"entre {min_pob:,} y {max_pob:,}"
        elif min_pob is not None:
            rango_str = f"mayor o igual a {min_pob:,}"
        elif max_pob is not None:
            rango_str = f"menor o igual a {max_pob:,}"
        else:
            rango_str = "todos"
        mostrar_lista_paises(resultados, f"Países con población {rango_str}")
    else:
        print("No se encontraron países en ese rango de población.")


def opcion_filtrar_por_superficie():
    """Filtra países por rango de superficie."""
    global paises
    print("Filtrar por rango de superficie")

    if not paises:
        print("No hay países cargados.")
        return

    # Solicitar mínimo
    min_str = input("Superficie mínima en km² (presione Enter para omitir): ")
    min_sup = None
    if min_str.strip():
        valido, valor = validar_entero_positivo(min_str)
        if valido:
            min_sup = valor
        else:
            print(f"Error en mínimo: {valor}")
            return

    # Solicitar máximo
    max_str = input("Superficie máxima en km² (presione Enter para omitir): ")
    max_sup = None
    if max_str.strip():
        valido, valor = validar_entero_positivo(max_str)
        if valido:
            max_sup = valor
        else:
            print(f"Error en máximo: {valor}")
            return

    # Verificar que mínimo <= máximo
    if min_sup is not None and max_sup is not None and min_sup > max_sup:
        print("Error: La superficie mínima no puede ser mayor que la máxima.")
        return

    # Filtrar
    resultados = []
    for p in paises:
        cumple = True
        if min_sup is not None and p['superficie'] < min_sup:
            cumple = False
        if max_sup is not None and p['superficie'] > max_sup:
            cumple = False
        if cumple:
            resultados.append(p)

    if resultados:
        rango_str = ""
        if min_sup is not None and max_sup is not None:
            rango_str = f"entre {min_sup:,} y {max_sup:,}"
        elif min_sup is not None:
            rango_str = f"mayor o igual a {min_sup:,}"
        elif max_sup is not None:
            rango_str = f"menor o igual a {max_sup:,}"
        else:
            rango_str = "todos"
        mostrar_lista_paises(resultados, f"Países con superficie {rango_str} km²")
    else:
        print("No se encontraron países en ese rango de superficie.")


def opcion_ordenar():
    """Ordena países por nombre, población o superficie."""
    global paises
    print("Ordenar países")

    if not paises:
        print("No hay países cargados.")
        return

    # Elegir criterio
    opciones_criterio = {
        '1': 'Nombre',
        '2': 'Población',
        '3': 'Superficie'
    }
    criterio = elegir_opcion("Seleccione el criterio de ordenamiento:", opciones_criterio)

    # Elegir orden
    opciones_orden = {
        '1': 'Ascendente (menor a mayor)',
        '2': 'Descendente (mayor a menor)'
    }
    orden = elegir_opcion("Seleccione el orden:", opciones_orden)

    # Determinar clave y reverse
    if criterio == '1':
        clave = 'nombre'
    elif criterio == '2':
        clave = 'poblacion'
    else:  # '3'
        clave = 'superficie'

    reverse = (orden == '2')  # Descendente si orden es '2'

    # Ordenar (crea una nueva lista para no modificar la original)
    paises_ordenados = sorted(paises, key=lambda x: x[clave], reverse=reverse)
    # Mostrar
    titulo = f"Países ordenados por {opciones_criterio[criterio].lower()} ({'descendente' if reverse else 'ascendente'})"
    mostrar_lista_paises(paises_ordenados, titulo)


def opcion_estadisticas():
  #Muestra estadísticas básicas: máximos, mínimos, promedios y conteo por continente.
    global paises
    print("Estadísticas")

    if not paises:
        print("No hay países cargados.")
        return

    #País con mayor y menor población
    mayor_pob = max(paises, key=lambda x: x['poblacion'])
    menor_pob = min(paises, key=lambda x: x['poblacion'])

    #Promedio de población
    suma_pob = sum(p['poblacion'] for p in paises)
    promedio_pob = suma_pob / len(paises)

    #Promedio de superficie
    suma_sup = sum(p['superficie'] for p in paises)
    promedio_sup = suma_sup / len(paises)

    #Cantidad de países por continente
    continentes = {}
    for p in paises:
        cont = p['continente']
        continentes[cont] = continentes.get(cont, 0) + 1

    # Mostrar resultados
    print("Estadísticas de países")

    print(f"Población:")
    print(f"  País con mayor población: {mayor_pob['nombre']} ({mayor_pob['poblacion']:,} habitantes)")
    print(f"  País con menor población: {menor_pob['nombre']} ({menor_pob['poblacion']:,} habitantes)")
    print(f"  Promedio de población: {promedio_pob:,.0f} habitantes")

    print(f"Superficie:")
    print(f"  Promedio de superficie: {promedio_sup:,.0f} km²")

    print(f"Cantidad de países por continente:")
    for cont, cantidad in sorted(continentes.items()):
        print(f"  {cont}: {cantidad} país(es)")

# Menú Principal

def mostrar_menu():
    print("Sistema de gestión de paises")
    print("1. Agregar país")
    print("2. Actualizar país")
    print("3. Buscar país por nombre")
    print("4. Filtrar países")
    print("5. Ordenar países")
    print("6. Estadísticas")
    print("7. Guardar y salir")


def opcion_filtrar():
    #Submenú para filtrar países.
    global paises
    if not paises:
        print("No hay países cargados.")
        return

    opciones = {
        '1': 'Por continente',
        '2': 'Por rango de población',
        '3': 'Por rango de superficie',
        '4': 'Volver al menú principal'
    }
    eleccion = elegir_opcion("Seleccione el tipo de filtro:", opciones)

    if eleccion == '1':
        opcion_filtrar_por_continente()
    elif eleccion == '2':
        opcion_filtrar_por_poblacion()
    elif eleccion == '3':
        opcion_filtrar_por_superficie()
    # '4' no hace nada, vuelve al menú principal


def main():
    #Función principal que ejecuta el bucle del menú.
    global paises

    inicializar_datos()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-7): ").strip()

        if opcion == '1':
            opcion_agregar_pais()
        elif opcion == '2':
            opcion_actualizar_pais()
        elif opcion == '3':
            opcion_buscar_pais()
        elif opcion == '4':
            opcion_filtrar()
        elif opcion == '5':
            opcion_ordenar()
        elif opcion == '6':
            opcion_estadisticas()
        elif opcion == '7':
            guardar_y_salir()
        else:
            print("Opción inválida. Por favor, seleccione un número del 1 al 7.")


# Punto de entrada si se ejecuta directamente
if __name__ == "__main__":
    main()
