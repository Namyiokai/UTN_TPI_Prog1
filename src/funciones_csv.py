import csv
import os

def cargar_datos(ruta_archivo):
    """
    Lee un archivo CSV y devuelve una lista de diccionarios.
    Cada diccionario representa un país con las claves:
    'nombre', 'poblacion', 'superficie', 'continente'.

    Args:
        ruta_archivo (str): Ruta al archivo CSV.

    Returns:
        list: Lista de diccionarios con los datos cargados.
              Si el archivo no existe o está vacío, retorna lista vacía.
    """
    # Verificar si el archivo existe
    if not os.path.exists(ruta_archivo): #Si el archivo no existe, retorna una lista vacía.
        print(f"El archivo {ruta_archivo} no existe.")
        return []

    paises = []

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo) #Lee el CSV y automáticamente usa la primera fila como nombres de columnas. Cada fila se vuelve en un diccionario. 

            # Validar que las columnas necesarias estén presentes
            columnas_requeridas = {'nombre', 'poblacion', 'superficie', 'continente'}
            if not columnas_requeridas.issubset(lector.fieldnames):
                print("Error: El CSV no tiene las columnas requeridas.")
                print(f"Columnas esperadas: {columnas_requeridas}")
                print(f"Columnas encontradas: {lector.fieldnames}")
                return []

            for fila in lector:
                try:
                    # Convertir tipos de datos
                    # Población y superficie deben ser enteros
                    # Usamos int() y manejamos posibles errores de formato
                    pais = {
                        'nombre': fila['nombre'].strip(),
                        'poblacion': int(fila['poblacion'].strip()), 
                        'superficie': int(float(fila['superficie'].strip())),  
                        'continente': fila['continente'].strip()
                    }
                    paises.append(pais)
                except ValueError as e:
                    print(f"Error en la fila {lector.line_num}: {fila}")
                    print(f"Detalle: {e} - Se omite esta fila.")
                except KeyError as e:
                    print(f"Falta una columna en la fila {lector.line_num}: {e}")
                    print(f"Se omite esta fila.")
    except Exception as e:
        print(f"Error inesperado al leer el archivo: {e}")
        return []

    print(f"{len(paises)} países cargados correctamente desde {ruta_archivo}")
    return paises


def guardar_datos(ruta_archivo, paises):
    """
    Guarda una lista de diccionarios en un archivo CSV.
    Sobrescribe el archivo si ya existe.

    Args:
        ruta_archivo (str): Ruta donde se guardará el archivo CSV.
        paises (list): Lista de diccionarios con los datos de los países.

    Returns:
        bool: True si se guardó correctamente, False en caso contrario.
    """
    if not paises:
        print("La lista de países está vacía. No se guarda nada.")
        return False

    # Asegurar que la carpeta exista
    directorio = os.path.dirname(ruta_archivo)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)

    try:
        with open(ruta_archivo, 'w', encoding='utf-8', newline='') as archivo:
            campos = ['nombre', 'poblacion', 'superficie', 'continente']
            writer = csv.DictWriter(archivo, fieldnames=campos)

            # Escribir encabezado
            writer.writeheader()

            # Escribir cada país
            for pais in paises:
                # Asegurar que todos los diccionarios tengan las claves correctas
                fila = {
                    'nombre': pais.get('nombre', ''),
                    'poblacion': pais.get('poblacion', 0),
                    'superficie': pais.get('superficie', 0),
                    'continente': pais.get('continente', '')
                }
                writer.writerow(fila)

        print(f"Datos guardados exitosamente en {ruta_archivo} ({len(paises)} países)")
        return True
    except PermissionError:
        print(f"No hay permisos para escribir en {ruta_archivo}")
        return False
    except Exception as e:
        print(f"Error inesperado al guardar: {e}")
        return False
    
