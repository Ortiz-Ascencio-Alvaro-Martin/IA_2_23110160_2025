# =================================================================
# Algoritmo de Dijkstra Simplificado (Búsqueda de Ruta Óptima)
# Esencialmente, UCS es una variante del algoritmo de Dijkstra.
# =================================================================

import heapq # Usamos heapq para manejar una cola de prioridad eficientemente.

def _reconstruir_ruta(predecesores, punto_final):
    """
    Función auxiliar para trazar el camino desde el final hasta el inicio
    usando el diccionario de predecesores.
    """
    camino_recorrido = []
    paso_actual = punto_final
    # Mientras no lleguemos al punto de partida (que no tiene predecesor).
    while paso_actual is not None:
        camino_recorrido.append(paso_actual)
        paso_actual = predecesores.get(paso_actual)
    # El camino está en orden inverso (destino -> origen), así que lo volteamos.
    return camino_recorrido[::-1]

def encontrar_ruta_de_costo_minimo(mapa, origen, destino):
    """
    Calcula el camino más "barato" (con menor costo acumulado) desde un
    origen a un destino en un mapa ponderado.
    """
    
    # 1. La "frontera" es una cola de prioridad. Almacena tuplas de (costo_total, ubicacion).
    #    heapq siempre mantendrá el elemento con el costo más bajo en la primera posición.
    frontera = [(0, origen)]
    
    # 2. Diccionario para registrar el "predecesor" de cada ubicación,
    #    esencialmente, cómo llegamos a ella. Sirve para reconstruir la ruta.
    predecesores = {origen: None}
    
    # 3. Diccionario para llevar la cuenta del costo mínimo conocido para
    #    llegar a cada ubicación desde el origen.
    distancias = {origen: 0}

    # 4. El bucle principal se ejecuta mientras haya ubicaciones por explorar en la frontera.
    while frontera:
        
        # 5. Obtenemos la ubicación en la frontera que tiene el menor costo acumulado hasta ahora.
        distancia_actual, ubicacion_actual = heapq.heappop(frontera)
        
        # 6. Si la ubicación que sacamos es nuestro destino, hemos encontrado la ruta más corta posible.
        if ubicacion_actual == destino:
            ruta_final = _reconstruir_ruta(predecesores, destino)
            return {
                "mensaje": f"Ruta óptima a '{destino}' encontrada.",
                "costo_total": distancia_actual,
                "ruta": " -> ".join(ruta_final)
            }

        # 7. Si no es el destino, exploramos sus puntos adyacentes (vecinos).
        for punto_siguiente, costo_del_tramo in mapa.get(ubicacion_actual, {}).items():
            
            # 8. Calculamos el costo que nos tomaría llegar al punto_siguiente a través de la ubicacion_actual.
            nueva_distancia_acumulada = distancia_actual + costo_del_tramo
            
            # 9. Esta es la condición clave: si el nuevo camino hacia punto_siguiente es más barato
            #    que cualquier otro camino que hayamos encontrado antes (o si es la primera vez que lo visitamos)...
            if punto_siguiente not in distancias or nueva_distancia_acumulada < distancias[punto_siguiente]:
                
                # 10. ...actualizamos los registros con esta nueva ruta óptima.
                distancias[punto_siguiente] = nueva_distancia_acumulada
                predecesores[punto_siguiente] = ubicacion_actual
                
                # 11. Y añadimos el punto_siguiente a la frontera para que sea considerado en futuras exploraciones.
                heapq.heappush(frontera, (nueva_distancia_acumulada, punto_siguiente))

    # 12. Si el bucle termina, la frontera se vació y nunca alcanzamos el destino.
    return {"mensaje": f"No se pudo encontrar una ruta desde '{origen}' hasta '{destino}'."}


# --- Ejemplo de Uso ---
# Definición del grafo: Ubicacion -> {Destino_Adyacente: Costo_Viaje}
mapa_con_costos = {
    'A': {'B': 1, 'C': 4},
    'B': {'D': 5, 'E': 2},
    'C': {'F': 3},
    'D': {'G': 1},
    'E': {'G': 8},
    'F': {},
    'G': {} # Destino
}

resultado_modificado = encontrar_ruta_de_costo_minimo(mapa_con_costos, 'A', 'G')

print("Grafo con costos (Mapa):")
for nodo, vecinos in mapa_con_costos.items():
    print(f"  {nodo}: {vecinos}")
print("-" * 30)
print(f"Resultado de la búsqueda UCS (A → G):")
for clave, valor in resultado_modificado.items():
    print(f"  - {clave.capitalize()}: {valor}")