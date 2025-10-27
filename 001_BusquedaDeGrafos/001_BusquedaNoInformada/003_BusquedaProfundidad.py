# =================================================================
# Exploración Profunda de un Laberinto (Implementación Recursiva de DFS)
# =================================================================

def explorar_camino_profundo(laberinto, posicion_actual, destino, visitados):
    """
    Función recursiva que explora un camino tan lejos como sea posible.
    Retorna True si encuentra el destino, False en caso contrario.
    """
    
    # 1. Marcamos la posición actual como visitada para no volver a pasar por ella
    #    en esta misma ruta y evitar ciclos infinitos.
    visitados.add(posicion_actual)

    # 2. Condición de éxito: si la posición actual es el destino, hemos terminado.
    if posicion_actual == destino:
        return True

    # 3. Para cada conexión (pasaje o vecino) desde la posición actual...
    for siguiente_paso in laberinto.get(posicion_actual, []):
        
        # 4. ...verificamos si ya hemos estado en ese siguiente paso.
        if siguiente_paso not in visitados:
            
            # 5. Si no hemos estado, nos adentramos en ese camino llamando a la función
            #    de nuevo desde esa nueva posición. Esto es la RECURSIÓN.
            #    Si esa llamada recursiva encuentra el destino, propagamos el éxito (True) hacia arriba.
            if explorar_camino_profundo(laberinto, siguiente_paso, destino, visitados):
                return True
    
    # 6. Si hemos explorado todos los caminos desde la posición actual y ninguno
    #    llegó al destino, significa que este es un callejón sin salida. Retrocedemos.
    return False

def iniciar_busqueda_profunda(laberinto, inicio, destino):
    """
    Función principal que prepara e inicia la búsqueda recursiva.
    """
    # Se crea un conjunto vacío para llevar el registro de los lugares visitados.
    # Este conjunto se pasará como referencia a través de todas las llamadas recursivas.
    lugares_visitados = set()
    
    # Inicia la exploración y comprueba el resultado booleano.
    encontrado = explorar_camino_profundo(laberinto, inicio, destino, lugares_visitados)
    
    if encontrado:
        return f"Éxito: Se encontró una ruta hacia '{destino}'."
    else:
        return f"Fracaso: El destino '{destino}' es inalcanzable desde el inicio."


# --- Ejemplo de Uso ---
# Definición del grafo (laberinto)
mapa_simple = {
    'A': ['B', 'C'], 
    'B': ['D'],
    'C': ['E', 'F'],
    'D': [],
    'E': ['G'],
    'F': [],
    'G': [] # Destino
}

print(f"Grafo (Mapa): {mapa_simple}")
resultado_modificado = iniciar_busqueda_profunda(mapa_simple, 'A', 'G')
print(f"Resultado de la búsqueda DFS Recursiva (A → G): {resultado_modificado}")
#