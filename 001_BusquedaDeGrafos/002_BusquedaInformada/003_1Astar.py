# =================================================================
# Planificador de Rutas Inteligente (Implementación OOP de A*)
# =================================================================

import heapq

class NavegadorAEstrella:
    """
    Encapsula el algoritmo A* para encontrar la ruta de menor costo en una red.
    A* es inteligente porque balancea el costo real del camino recorrido (g(n))
    con una estimación del costo restante hasta la meta (h(n)).
    
    Prioridad de Búsqueda: f(n) = g(n) + h(n)
    """

    def __init__(self, red, heuristica):
        """Inicializa el navegador con la red de rutas y las estimaciones."""
        self.red = red
        self.heuristica = heuristica

    def _reconstruir_ruta(self, predecesores, meta):
        """Función auxiliar para trazar el camino óptimo hacia atrás."""
        ruta = []
        paso = meta
        while paso is not None:
            ruta.append(paso)
            paso = predecesores.get(paso)
        return list(reversed(ruta))

    def encontrar_ruta_optima(self, inicio, meta):
        """
        Ejecuta el algoritmo A* para encontrar el camino más barato desde
        el inicio hasta la meta.
        """
        # 1. La frontera (cola de prioridad) almacena tuplas de (f(n), ubicacion).
        #    f(n) = g(n) + h(n). Inicialmente, g(n) es 0.
        frontera = [(self.heuristica[inicio], inicio)]
        
        # 2. Diccionario para registrar los predecesores de cada nodo en la ruta óptima.
        predecesores = {inicio: None}
        
        # 3. g(n): Diccionario para almacenar el costo REAL más bajo encontrado
        #    desde el inicio hasta cada ubicación.
        costo_g = {inicio: 0}

        while frontera:
            # 4. Se extrae el nodo de la frontera con el menor costo f(n).
            #    Este es el nodo más prometedor para explorar a continuación.
            f_actual, posicion_actual = heapq.heappop(frontera)

            # 5. Si hemos llegado a la meta, reconstruimos la ruta y terminamos.
            if posicion_actual == meta:
                ruta_final = self._reconstruir_ruta(predecesores, meta)
                costo_final = costo_g[meta]
                return {
                    "mensaje": f"¡Ruta óptima a '{meta}' encontrada!",
                    "ruta": " → ".join(ruta_final),
                    "costo": costo_final
                }

            # 6. Se exploran las conexiones (vecinos) de la posición actual.
            for vecino, costo_tramo in self.red.get(posicion_actual, {}).items():
                
                # 7. Se calcula el costo g(n) para el vecino a través de la ruta actual.
                nuevo_costo_g = costo_g[posicion_actual] + costo_tramo
                
                # 8. Condición clave de A*: Si esta nueva ruta al vecino es más barata
                #    que cualquier otra encontrada antes (o si es la primera vez que lo vemos)...
                if vecino not in costo_g or nuevo_costo_g < costo_g[vecino]:
                    
                    # 9. ...se actualizan sus registros.
                    predecesores[vecino] = posicion_actual
                    costo_g[vecino] = nuevo_costo_g
                    
                    # 10. Se calcula su costo total estimado f(n) = g(n) + h(n).
                    estimacion_h = self.heuristica.get(vecino, 0)
                    costo_f = nuevo_costo_g + estimacion_h
                    
                    # 11. Y se añade a la frontera para ser considerado en futuras exploraciones.
                    heapq.heappush(frontera, (costo_f, vecino))
                    
        return {"mensaje": "Búsqueda fallida. No se encontró una ruta."}


# --- Datos del Problema ---
# El mapa con los costos reales de cada tramo.
mapa_costos = {
    'A': {'B': 1, 'C': 4}, 'B': {'D': 5, 'E': 2}, 'C': {'F': 3},
    'D': {'G': 1}, 'E': {'G': 8}, 'F': {}, 'G': {}
}

# La "intuición" del algoritmo: estimación de la distancia de cada punto a 'G'.
heuristica_hacia_g = {
    'A': 8, 'B': 5, 'C': 5, 'D': 1, 'E': 2, 'F': 4, 'G': 0
}

INICIO = 'A'
OBJETIVO = 'G'

print(f"Grafo (Costos Reales): {mapa_costos}")
print(f"Heurística h(n) hacia '{OBJETIVO}': {heuristica_hacia_g}")
print("-" * 50)

# --- Ejecución del Algoritmo ---
# 1. Se crea una instancia del navegador con el mapa y las heurísticas.
navegador = NavegadorAEstrella(mapa_costos, heuristica_hacia_g)
# 2. Se ejecuta la búsqueda.
resultado = navegador.encontrar_ruta_optima(INICIO, OBJETIVO)

print(f"Resultado de la Búsqueda A* ({INICIO} → {OBJETIVO}):")
for clave, valor in resultado.items():
    print(f"  - {clave.capitalize()}: {valor}")