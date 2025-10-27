# ====================================================================
# Recorrido de Grafos por Niveles (Implementación Alternativa de BFS)
# ====================================================================

def explorar_red_por_amplitud(red_de_nodos, punto_partida, meta):
    """
    Esta función determina si existe una ruta desde un punto de partida
    hasta una meta en una red (grafo), explorando nivel por nivel.
    """

    # 1. Creamos una lista que funcionará como nuestra "frontera" de exploración.
    #    Inicia con el primer nodo a visitar, que es el punto de partida.
    #    Usamos una lista estándar como si fuera una cola (FIFO: First-In, First-Out).
    frontera = [punto_partida]
    
    # 2. Usamos un conjunto para guardar un registro de los nodos que ya hemos
    #    considerado. Esto es crucial para no procesar el mismo nodo dos veces
    #    y evitar bucles infinitos en grafos con ciclos.
    explorados = {punto_partida}

    # 3. El bucle principal se ejecuta mientras queden nodos en nuestra frontera.
    #    Si la frontera se vacía, significa que ya no hay más nodos alcanzables.
    while len(frontera) > 0:
        
        # 4. Sacamos el primer elemento de la lista. Esto asegura que exploremos
        #    en el orden en que encontramos los nodos (primero en amplitud).
        posicion_actual = frontera.pop(0)
        
        # 5. Verificamos si el nodo que estamos procesando es nuestra meta.
        if posicion_actual == meta:
            # Si lo es, hemos terminado exitosamente.
            return f"Misión cumplida: ¡Se ha localizado la meta '{meta}'!"
            
        # 6. Si no es la meta, buscamos todas las conexiones (vecinos)
        #    de nuestra posición actual para expandir la frontera.
        #    El .get() previene un error si un nodo no tiene conexiones definidas.
        for adyacente in red_de_nodos.get(posicion_actual, []):
            
            # 7. Para cada vecino, comprobamos si ya fue explorado antes.
            if adyacente not in explorados:
                
                # 8. Si es un nodo nuevo, lo añadimos al registro de explorados...
                explorados.add(adyacente)
                
                # 9. ...y lo agregamos al final de nuestra frontera para visitarlo
                #    en un futuro turno.
                frontera.append(adyacente)
    
    # 10. Si el bucle termina y nunca encontramos la meta, significa que
    #     no es alcanzable desde el punto de partida.
    return f"Búsqueda fallida: La meta '{meta}' es inalcanzable."

# --- Ejemplo de Uso ---
# Definición de un grafo simple para el ejemplo
mapa_simple = {
    'A': ['B', 'C'], # Desde A puedes ir a B y C
    'B': ['D'],
    'C': ['E', 'F'],
    'D': [],
    'E': ['G'],
    'F': [],
    'G': []          # Meta
}

# Ejecución de la función modificada
print(f"Grafo (Mapa): {mapa_simple}")
resultado_modificado = explorar_red_por_amplitud(mapa_simple, 'A', 'G')
print(f"Resultado de la búsqueda (A → G): {resultado_modificado}")