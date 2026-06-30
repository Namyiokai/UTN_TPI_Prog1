
import re # Importar la librería re para expresiones regulares

def validar_entero_positivo(valor):
    try:
        # Convertir a entero
        num = int(valor)
        if num <= 0:
            return False, "El valor debe ser un número entero positivo mayor a 0."
        return True, num
    except ValueError:
        return False, "Debe ingresar un número entero válido."


def validar_float_positivo(valor):
    try:
        num = float(valor)
        if num <= 0:
            return False, "El valor debe ser un número positivo mayor a 0."
        return True, num
    except ValueError:
        return False, "Debe ingresar un número válido."


def validar_texto_no_vacio(texto):

    if not texto or texto.strip() == "":
        return False, "El campo no puede estar vacío."
    return True, texto.strip()

def validar_nombre_pais(nombre):
    """
    Valida que el nombre de un país contenga solo letras y espacios, y no esté vacío.
    """
    # Primero, validar que el nombre no esté vacío, eliminando espacios al inicio y al final
    if not nombre or nombre.strip() == "":
        return False, "El nombre del país no puede estar vacío."

    nombre_limpio = nombre.strip()
    
    # Iterar sobre cada carácter del nombre limpio
    for caracter in nombre_limpio:
        # Verificar si el carácter no es una letra Y no es un espacio
        # .isalpha() verifica si el carácter es una letra (maneja acentos y 'ñ' en Python 3)
        # .isspace() verifica si el carácter es un espacio en blanco
        if not (caracter.isalpha() or caracter.isspace()):
            # Si encontramos algo que no es letra ni espacio, el nombre no es válido
            return False, "El nombre del país solo puede contener letras y espacios."
            
    # Si el bucle termina, significa que todos los caracteres eran válidos
    return True, nombre_limpio


def buscar_pais_por_nombre(paises, texto_busqueda):

    if not texto_busqueda or texto_busqueda.strip() == "":
        return []

    texto_busqueda = texto_busqueda.lower().strip()
    resultados = []

    for pais in paises:
        nombre = pais.get('nombre', '').lower()
        if texto_busqueda in nombre:
            resultados.append(pais)

    return resultados


def mostrar_pais(pais, numero=None):

    if numero:
        print(f"{numero}. {pais['nombre']} - Población: {pais['poblacion']:,} | Superficie: {pais['superficie']:,} km² | Continente: {pais['continente']}")
    else:
        print(f"{pais['nombre']} - Población: {pais['poblacion']:,} | Superficie: {pais['superficie']:,} km² | Continente: {pais['continente']}")


def mostrar_lista_paises(paises, titulo="Lista de países"):

    if not paises:
        print("No hay países para mostrar.")
        return

    print(f"{titulo} (Total: {len(paises)})")

    for i, pais in enumerate(paises, 1):
        mostrar_pais(pais, i)


def obtener_continentes_unicos(paises):
    continentes = set()
    for pais in paises:
        continente = pais.get('continente', '').strip()
        if continente:
            continentes.add(continente)
    return sorted(list(continentes))


def mostrar_continentes_disponibles(paises):
    continentes = obtener_continentes_unicos(paises)
    if not continentes:
        print("No hay continentes disponibles en los datos.")
        return False

    print("Continentes disponibles:")
    for i, continente in enumerate(continentes, 1):
        print(f"{i}.{continente}")
    return True


def solicitar_entero(mensaje, mensaje_error="Debe ingresar un número entero válido."):
    while True:
        try:
            valor = input(mensaje)
            if not valor:
                print("No puede estar vacío. Intente nuevamente.")
                continue
            return int(valor)
        except ValueError:
            print(f"{mensaje_error}")


def solicitar_texto(mensaje, mensaje_error="El campo no puede estar vacío."):
    while True:
        valor = input(mensaje)
        if valor and valor.strip():
            return valor.strip()
        print(f"{mensaje_error}")


def elegir_opcion(mensaje, opciones):
    print(f"{mensaje}")
    for clave, descripcion in opciones.items():
        print(f"  {clave}. {descripcion}")

    while True:
        eleccion = input("Seleccione una opción: ").strip()
        if eleccion in opciones:
            return eleccion
        print("Opción inválida. Intente nuevamente.")
