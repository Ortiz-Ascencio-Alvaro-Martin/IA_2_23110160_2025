# =========================================================================
# Navegación Guiada por Estimación (Greedy Best-First Search)
# =========================================================================

import heapq # Para manejar la cola de prioridad de forma eficiente.

def _reconstruir_camino(predecesores, punto_final):
    """Función auxiliar para trazar la ruta desde el final hasta el inicio."""
    camino = []
    paso_actual = punto_final
    while paso_actual is not None:
        camino.append(paso_actual)
        paso_actual = predecesores.get(paso_actual)
    # El camino se construye al revés, así que lo invertimos para el orden correcto.
    return list(reversed(camino))

def encontrar_ruta_mas_prometedora(red_de_rutas, estimaciones_h, punto_partida, meta):
    """
    Implementa la Búsqueda Voraz. Este algoritmo es "miope" y siempre elige
    el camino que PARECE más corto hacia el objetivo, basándose únicamente
    en la heurística h(n), sin considerar el costo del camino ya recorrido.
    """
    
    # 1. La cola de prioridad almacenará tuplas de (valor_heuristico, ubicacion).
    #    heapq se asegurará de que el elemento con el menor valor heurístico siempre esté al frente.
    frontera_de_busqueda = [(estimaciones_h[punto_partida], punto_partida)]
    
    # 2. Diccionario para registrar el "predecesor" de cada ubicación,
    #    lo que nos permitirá reconstruir el camino al final.
    predecesores = {punto_partida: None}
    
    # 3. Conjunto para llevar un registro de las ubicaciones que ya han sido
    #    agregadas a la frontera, para no procesarlas dos veces.
    explorados = {punto_partida}

    # 4. El bucle principal continúa mientras haya opciones prometedoras en la frontera.
    while frontera_de_busqueda:
        
        # 5. Se extrae la ubicación que actualmente tiene la MEJOR (menor) estimación heurística.
        h_actual, posicion_actual = heapq.heappop(frontera_de_busqueda)
        
        print(f"  📍 Explorando: {posicion_actual} (Estimación h(n) = {h_actual})")

        # 6. Condición de éxito: Si la ubicación actual es la meta, hemos terminado.
        if posicion_actual == meta:
            ruta_encontrada = _reconstruir_camino(predecesores, meta)
            return f"¡Meta '{meta}' alcanzada! Ruta seguida: {' → '.join(ruta_encontrada)}"
            
        # 7. Se exploran las conexiones (vecinos) desde la posición actual.
        for siguiente_parada in red_de_rutas.get(posicion_actual, []):
            if siguiente_parada not in explorados:
                
                # 8. Se marca el vecino como explorado para no volver a considerarlo.
                explorados.add(siguiente_parada)
                
                # 9. Se registra que llegamos a 'siguiente_parada' desde 'posicion_actual'.
                predecesores[siguiente_parada] = posicion_actual
                
                # 10. Se añade el vecino a la frontera, usando SU PROPIO valor heurístico como prioridad.
                #     Esta es la esencia del algoritmo "voraz".
                h_vecino = estimaciones_h.get(siguiente_parada, float('inf'))
                heapq.heappush(frontera_de_busqueda, (h_vecino, siguiente_parada))
                
    # 11. Si la frontera se vacía, significa que no hay un camino posible.
    return "Búsqueda fallida: La meta es inalcanzable."


# --- Datos del Problema ---
# El mapa de conexiones entre puntos.
mapa_de_conexiones = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['E'],
    'D': ['E'],
    'E': ['F']  # Meta
}

# La "intuición" del algoritmo: una estimación de qué tan lejos está cada punto de la meta 'F'.
# Nota cómo 'C' (h=1) parece mucho más prometedor que 'B' (h=4).
estimaciones_al_objetivo = {
    'A': 5,
    'B': 4,
    'C': 1,
    'D': 2,
    'E': 1,
    'F': 0   # La meta siempre tiene una heurística de 0.
}

INICIO = 'A'
OBJETIVO = 'F'

print(f"Red de Rutas: {mapa_de_conexiones}")
print(f"Estimaciones Heurísticas (hacia '{OBJETIVO}'): {estimaciones_al_objetivo}")
print("-" * 50)
print(f"Iniciando Búsqueda Voraz ({INICIO} → {OBJETIVO}):")
resultado = encontrar_ruta_mas_prometedora(mapa_de_conexiones, estimaciones_al_objetivo, INICIO, OBJETIVO)

print("-" * 50)
print(f"Resultado final: {resultado}")
#