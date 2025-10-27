# =================================================================
# Heurísticas: Estimación h(n) con Distancia de Manhattan
# =================================================================

def calcular_distancia_manhattan(origen, destino):
    """
    Calcula la distancia de Manhattan (o "distancia de la ciudad").
    Esta es una función heurística h(n) muy común y eficiente.
    
    Imagina moverte por las calles de una cuadrícula: solo puedes ir
    hacia arriba/abajo o izquierda/derecha.
    
    h(n) = |x_destino - x_origen| + |y_destino - y_origen|
    """
    # Se extraen las coordenadas de los puntos de origen y destino.
    x_origen, y_origen = origen
    x_destino, y_destino = destino
    
    # 1. Se calcula la distancia horizontal (número de "bloques" en x).
    distancia_x = abs(x_destino - x_origen)
    
    # 2. Se calcula la distancia vertical (número de "bloques" en y).
    distancia_y = abs(y_destino - y_origen)
    
    # 3. La distancia total es la suma de ambos movimientos.
    return distancia_x + distancia_y

# --- Configuración del Problema ---

# 1. Coordenadas del punto al que queremos llegar.
DESTINO_FINAL = (10, 5)

# 2. Diccionario con las ubicaciones y sus coordenadas (x, y).
coordenadas_ciudades = {
    'Ciudad A': (3, 8),
    'Ciudad B': (12, 4), # Debería ser la más prometedora.
    'Ciudad C': (1, 1),
    'Ciudad D': (7, 6)
}

print(f"Punto de Destino: {DESTINO_FINAL}")
print("-" * 50)
print("Calculando la Heurística de Manhattan h(n) para cada ciudad:")

# 3. Se itera sobre cada ciudad para calcular su "promesa" (heurística).
estimaciones = {}
for ciudad, coords in coordenadas_ciudades.items():
    # Se calcula el valor heurístico para la ciudad actual.
    h_valor = calcular_distancia_manhattan(coords, DESTINO_FINAL)
    estimaciones[ciudad] = h_valor
    print(f"  h({ciudad} {coords}): {h_valor}")

print("-" * 50)

# 4. Se identifica la ciudad con la menor estimación de distancia.
mejor_opcion = min(estimaciones, key=estimaciones.get)
valor_minimo = estimaciones[mejor_opcion]

print(f"La opción más prometedora (con menor h(n)) es: {mejor_opcion}")
print(f"Su distancia de Manhattan estimada al destino es: {valor_minimo}")