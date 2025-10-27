# =========================================================================
# Búsqueda por Profundización Progresiva (Implementación Unificada de IDS)
# =========================================================================

def busqueda_profunda_progresiva(estructura, origen, objetivo, profundidad_maxima):
    """
    Implementa la Búsqueda en Profundidad Iterativa (IDS) usando un enfoque
    iterativo. Repite una búsqueda con límite de profundidad (DLS)
    aumentando el límite en cada pasada.
    
    Este método combina la eficiencia de memoria de DFS con la optimalidad
    de BFS (encuentra la ruta más corta en grafos no ponderados).
    """
    print(f"Iniciando búsqueda progresiva para '{objetivo}'...")

    # 1. Bucle principal de profundización:
    #    Itera desde una profundidad de 0 hasta la profundidad máxima permitida.
    for nivel_maximo in range(profundidad_maxima + 1):
        print(f"\n--- Iniciando barrido con profundidad máxima = {nivel_maximo} ---")
        
        # --- Inicio de la lógica DLS (Búsqueda en Profundidad Limitada) Iterativa ---
        
        # 2. Pila para la búsqueda actual. Almacena tuplas (nodo, nivel_actual).
        pila_busqueda = [(origen, 0)]
        
        # 3. Registro de nodos visitados para esta iteración.
        #    Es crucial REINICIARLO en cada nuevo nivel de profundidad para
        #    poder volver a explorar las mismas rutas, pero más a fondo.
        visitados_en_iteracion = {origen}

        # 4. Mientras haya nodos por explorar en la pila de este barrido...
        while pila_busqueda:
            posicion_actual, nivel_actual = pila_busqueda.pop()
            
            # 5. Condición de éxito: ¿Es el objetivo?
            if posicion_actual == objetivo:
                return f"¡Éxito! Objetivo '{objetivo}' hallado en el nivel {nivel_maximo}."

            # 6. Expansión: Si no hemos alcanzado el límite de este barrido,
            #    agregamos los vecinos a la pila.
            if nivel_actual < nivel_maximo:
                # Se itera en reversa para que el primer vecino en la lista sea
                # el primero en ser procesado (al hacer pop).
                for sucesor in reversed(estructura.get(posicion_actual, [])):
                    if sucesor not in visitados_en_iteracion:
                        visitados_en_iteracion.add(sucesor)
                        pila_busqueda.append((sucesor, nivel_actual + 1))
        
        # --- Fin de la lógica DLS ---
        # Si llegamos aquí, la búsqueda para el nivel_maximo actual terminó sin éxito.
        # El bucle for continuará con el siguiente nivel.

    # 7. Si el bucle principal termina, significa que exploramos hasta la
    #    profundidad_maxima y no se encontró el objetivo.
    return f"Búsqueda completa. El objetivo '{objetivo}' no fue encontrado con una profundidad máxima de {profundidad_maxima}."


# --- Ejemplo de Uso ---
# Definición de la estructura jerárquica (grafo)
mapa = {
    'A': ['B', 'C'], # Nivel 0
    'B': ['D'],      # Nivel 1
    'C': ['E', 'F'], # Nivel 1
    'D': ['G'],      # Nivel 2
    'E': [],
    'F': [],
    'G': []          # Nivel 3 (Objetivo)
}

# El objetivo 'G' se encuentra en la profundidad 3.
LIMITE_MAXIMO_PERMITIDO = 4

print(f"Grafo (Mapa): {mapa}")
resultado_modificado = busqueda_profunda_progresiva(mapa, 'A', 'G', LIMITE_MAXIMO_PERMITIDO)

print("\n" + "=" * 50)
print(f"Resultado final de la Búsqueda Progresiva: {resultado_modificado}")