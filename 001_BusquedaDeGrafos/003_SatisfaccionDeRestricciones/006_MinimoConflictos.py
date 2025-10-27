# =========================================================================
# Solucionador N-Reinas con Mínimos-Conflictos (Versión Simplificada)
# =========================================================================

import random

def resolver_con_min_conflictos(n=8, max_pasos=1000):
    """
    Resuelve el problema de las N-Reinas usando el algoritmo de Mínimos-Conflictos.
    Es una búsqueda local que intenta minimizar el número de reinas que se atacan.
    """

    # --- 1. Función de Evaluación (Más simple) ---
    def calcular_conflictos_totales(configuracion):
        """
        Cuenta el número total de pares de reinas que se atacan entre sí.
        El objetivo es que esta función devuelva 0.
        """
        conflictos = 0
        for i in range(n):
            for j in range(i + 1, n):
                # Conflicto en la misma fila
                if configuracion[i] == configuracion[j]:
                    conflictos += 1
                # Conflicto en la diagonal (distancia vertical == distancia horizontal)
                elif abs(i - j) == abs(configuracion[i] - configuracion[j]):
                    conflictos += 1
        return conflictos

    # --- 2. Inicialización ---
    # Se genera una configuración inicial aleatoria (una reina por columna).
    # El índice es la columna, el valor es la fila.
    configuracion_actual = [random.randint(0, n - 1) for _ in range(n)]
    
    # --- 3. Bucle Principal de Búsqueda ---
    for i in range(max_pasos):
        conflictos = calcular_conflictos_totales(configuracion_actual)
        
        # Condición de éxito: si no hay conflictos, hemos encontrado la solución.
        if conflictos == 0:
            print(f"Solución encontrada en el paso {i}.")
            return configuracion_actual

        # 4. Seleccionar una reina en conflicto al azar.
        # Primero, se identifican todas las reinas que participan en al menos un conflicto.
        reinas_en_conflicto = [
            col for col in range(n) if calcular_conflictos_totales(configuracion_actual) > 0
        ]
        
        # Se elige una de ellas al azar para moverla.
        reina_a_mover = random.choice(reinas_en_conflicto)
        
        # 5. Encontrar la mejor nueva posición para esa reina.
        # Se busca la fila que resulte en el menor número de conflictos totales.
        mejor_fila = -1
        min_conflictos = float('inf')
        
        for fila_potencial in range(n):
            # Se crea una copia temporal para probar el movimiento.
            configuracion_prueba = list(configuracion_actual)
            configuracion_prueba[reina_a_mover] = fila_potencial
            
            conflictos_prueba = calcular_conflictos_totales(configuracion_prueba)
            
            if conflictos_prueba < min_conflictos:
                min_conflictos = conflictos_prueba
                mejor_fila = fila_potencial
                
        # 6. Mover la reina a su nueva, mejor posición.
        configuracion_actual[reina_a_mover] = mejor_fila

    # Si el bucle termina, no se encontró una solución en los pasos permitidos.
    print(f"Búsqueda finalizada tras {max_pasos} pasos sin encontrar solución.")
    return configuracion_actual

# --- Ejecución ---
TAMANO_TABLERO = 8
solucion_encontrada = resolver_con_min_conflictos(n=TAMANO_TABLERO)

print("-" * 50)
print("Resultado Final:")
print(f"  Mejor configuración encontrada: {solucion_encontrada}")