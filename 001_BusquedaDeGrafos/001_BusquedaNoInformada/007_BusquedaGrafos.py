# =================================================================
# Representación de un Grafo (La Forma Más Simple)
# =================================================================

# Un grafo puede ser representado directamente con un diccionario.
# - Cada "clave" del diccionario es un "nodo" (una ubicación).
# - El "valor" asociado a cada clave es una "lista" de los nodos
#   a los que está conectado directamente (sus vecinos).

mapa = {
    'Aeropuerto': ['Ciudad_A', 'Ciudad_B'],
    'Ciudad_A':   ['Aeropuerto', 'Ciudad_C'],
    'Ciudad_B':   ['Aeropuerto', 'Ciudad_D'],
    'Ciudad_C':   ['Ciudad_A', 'Objetivo'],
    'Ciudad_D':   ['Ciudad_B', 'Ciudad_E'],
    'Ciudad_E':   ['Ciudad_D', 'Objetivo'],
    'Objetivo':   ['Ciudad_C', 'Ciudad_E']
}

# --- Puntos de la Tarea ---

INICIO = 'Aeropuerto'
OBJETIVO = 'Objetivo'

# --- Mostrar el Grafo ---
print("Grafo (Mapa de Ciudades):")

# Imprime el grafo de una forma legible
for ubicacion, conexiones in mapa.items():
    print(f"  - {ubicacion} está conectado con: {conexiones}")
    
print("-" * 40)
print(f"Tarea: Encontrar una ruta de '{INICIO}' a '{OBJETIVO}'")