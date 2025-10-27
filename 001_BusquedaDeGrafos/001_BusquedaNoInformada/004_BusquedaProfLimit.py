# ====================================================================
# Exploración de Rutas con Profundidad Controlada (DLS Iterativo)
# ====================================================================

def explorar_con_profundidad_maxima(red, punto_partida, meta, profundidad_limite):
    """
    Realiza una búsqueda en profundidad pero con una restricción: nunca
    explora más allá de un nivel de profundidad especificado. Usa una pila
    explícita para controlar el recorrido.
    """
    
    # 1. La pila almacenará tuplas de (nodo, profundidad_actual).
    #    Iniciamos con el punto de partida en profundidad 0.
    pila_de_exploracion = [(punto_partida, 0)]
    
    # 2. Usamos un conjunto para evitar volver a procesar el mismo nodo
    #    en la misma ruta y prevenir bucles.
    nodos_visitados = {punto_partida}

    # 3. El bucle se ejecuta mientras haya nodos pendientes en la pila.
    while pila_de_exploracion:
        
        # 4. Extraemos el último nodo agregado (LIFO), junto con su profundidad.
        nodo_actual, profundidad_actual = pila_de_exploracion.pop()
        
        print(f"  Explorando: {nodo_actual} (Nivel: {profundidad_actual})")

        # 5. Condición de éxito: Verificamos si hemos llegado a la meta.
        if nodo_actual == meta:
            return f"¡Meta '{meta}' localizada en el nivel {profundidad_actual}!"
        
        # 6. Condición de corte: Si no hemos alcanzado el límite de profundidad,
        #    podemos seguir explorando desde este nodo.
        if profundidad_actual < profundidad_limite:
            
            # 7. Obtenemos los vecinos y los recorremos en orden inverso para que
            #    al meterlos en la pila, el primero de la lista original sea
            #    el primero en ser explorado (simulando el orden de la recursión).
            for vecino in reversed(red.get(nodo_actual, [])):
                
                if vecino not in nodos_visitados:
                    # 8. Marcamos el vecino como visitado...
                    nodos_visitados.add(vecino)
                    # ...y lo añadimos a la pila con su nueva profundidad.
                    pila_de_exploracion.append((vecino, profundidad_actual + 1))

    # 9. Si el bucle termina, la pila se vació y no encontramos la meta dentro del límite.
    return f"Búsqueda finalizada. La meta '{meta}' no se encontró dentro del límite de {profundidad_limite} niveles."

# --- Ejemplo de Uso ---
# Definición del grafo:
mapa_profundo = {
    'A': ['B', 'C'], # Nivel 0
    'B': ['D'],      # Nivel 1
    'C': ['E', 'F'], # Nivel 1
    'D': ['G'],      # Nivel 2
    'E': [],
    'F': [],
    'G': []          # Nivel 3 (Meta)
}

# La profundidad real de 'G' es 3. Si ponemos 2, no lo encontrará.
# Si ponemos 3 o más, sí lo encontrará.
LIMITE_DE_BUSQUEDA = 3

print(f"Grafo (Mapa): {mapa_profundo}")
print(f"Límite de Profundidad Máxima: {LIMITE_DE_BUSQUEDA}")
print("-" * 40)

resultado_modificado = explorar_con_profundidad_maxima(mapa_profundo, 'A', 'G', LIMITE_DE_BUSQUEDA)

print("-" * 40)
print(f"Resultado final DLS Iterativo: {resultado_modificado}")