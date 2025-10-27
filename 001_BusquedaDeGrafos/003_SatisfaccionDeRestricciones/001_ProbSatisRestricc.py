# =========================================================================
# Problema de Satisfacción de Restricciones (CSP) - Versión Simplificada
# =========================================================================

# --- 1. DEFINICIÓN DEL PROBLEMA ---

# Variables: Los países a colorear.
PAISES = ['A', 'B', 'C']

# Dominios: Los colores disponibles para cada país.
COLORES_DISPONIBLES = ['Rojo', 'Verde']

# Restricciones: Qué países son vecinos y no pueden tener el mismo color.
# Usamos un diccionario para un acceso más directo (A es vecino de B y C, etc.).
VECINOS = {
    'A': ['B', 'C'],
    'B': ['A'],
    'C': ['A']
}

# --- 2. FUNCIÓN DE VALIDACIÓN (Más simple) ---

def es_valido(pais, color, asignacion_actual):
    """
    Verifica si asignar un 'color' a un 'pais' es válido,
    considerando las asignaciones ya hechas.
    """
    # Revisa cada vecino del país actual.
    for vecino in VECINOS.get(pais, []):
        # Si el vecino ya tiene un color asignado y es el mismo que estamos intentando usar...
        if vecino in asignacion_actual and asignacion_actual[vecino] == color:
            # ...entonces no es una asignación válida.
            return False
    # Si no se encontraron conflictos con ningún vecino, la asignación es válida.
    return True

# --- 3. ALGORITMO DE BÚSQUEDA CON VUELTA ATRÁS ---

def resolver_csp(asignacion={}):
    """
    Función recursiva de backtracking para encontrar una solución.
    """
    # Caso Base: Si todos los países tienen color, encontramos una solución.
    if len(asignacion) == len(PAISES):
        return asignacion

    # 1. Seleccionar el siguiente país sin color.
    pais_a_colorear = next(p for p in PAISES if p not in asignacion)

    # 2. Intentar asignar cada color disponible.
    for color in COLORES_DISPONIBLES:
        # 3. Verificar si la asignación es válida.
        if es_valido(pais_a_colorear, color, asignacion):
            
            # Si es válida, la aplicamos.
            asignacion[pais_a_colorear] = color
            
            # Llamamos a la función de nuevo para el siguiente país.
            resultado = resolver_csp(asignacion)
            
            # Si la llamada recursiva encontró una solución completa, la propagamos.
            if resultado:
                return resultado
            
            # 4. Vuelta Atrás (Backtrack): Si no se encontró solución,
            #    deshacemos la asignación y probamos el siguiente color.
            del asignacion[pais_a_colorear]
            
    # Si probamos todos los colores y ninguno funcionó, no hay solución en esta rama.
    return None

# --- EJECUCIÓN ---
print("Buscando una solución para colorear el mapa...")
solucion = resolver_csp()

print("-" * 50)
if solucion:
    print(" ¡Solución encontrada!")
    # Imprime el resultado de forma clara.
    for pais, color in solucion.items():
        print(f"  - País {pais}: {color}")
else:
    print(" No se pudo encontrar una solución.")