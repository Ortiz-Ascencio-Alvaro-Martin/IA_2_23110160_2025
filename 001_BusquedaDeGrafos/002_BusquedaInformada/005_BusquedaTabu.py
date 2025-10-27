# =================================================================
# Búsqueda Tabú Simplificada para N-Reinas
# Objetivo: Minimizar el número de ataques a 0.
# =================================================================

import random
from collections import deque

def contar_conflictos(tablero):
    """
    Función de evaluación más simple: cuenta el número de pares de reinas
    que se atacan directamente en las diagonales. El objetivo es 0.
    """
    conflictos = 0
    n = len(tablero)
    for i in range(n):
        for j in range(i + 1, n):
            # abs(col1 - col2) == abs(row1 - row2) indica un ataque diagonal.
            if abs(i - j) == abs(tablero[i] - tablero[j]):
                conflictos += 1
    return conflictos

def resolver_n_reinas_tabu(n=8, tenencia=7, max_iter=1000):
    """
    Implementa la Búsqueda Tabú de una forma más concisa.
    """
    # 1. ESTADO INICIAL
    # Se genera un tablero aleatorio. Cada índice es una columna, y el valor es la fila.
    tablero_actual = [random.randint(0, n - 1) for _ in range(n)]
    
    # Se guarda el mejor tablero encontrado hasta ahora.
    mejor_tablero = list(tablero_actual)
    mejor_conflictos = contar_conflictos(mejor_tablero)
    
    # 2. MEMORIA TABÚ
    # Usamos una deque con longitud máxima para manejar la lista tabú automáticamente.
    # Almacenará los "movimientos" prohibidos: (columna, nueva_fila).
    lista_tabu = deque(maxlen=tenencia)

    print(f"Inicio: {tablero_actual} (Conflictos: {mejor_conflictos})")

    # 3. BUCLE DE BÚSQUEDA
    for _ in range(max_iter):
        
        # Si ya encontramos la solución, nos detenemos.
        if mejor_conflictos == 0:
            break

        mejor_movimiento = None
        mejor_vecino_conflictos = float('inf') # Buscamos minimizar, empezamos en infinito.

        # 4. EXPLORACIÓN DEL VECINDARIO
        # Un "movimiento" es mover una reina de una columna a una nueva fila.
        for col in range(n):
            fila_original = tablero_actual[col]
            for nueva_fila in range(n):
                if fila_original == nueva_fila:
                    continue # No es un movimiento real.

                # Realiza el movimiento temporalmente.
                tablero_actual[col] = nueva_fila
                conflictos_actuales = contar_conflictos(tablero_actual)
                movimiento = (col, nueva_fila)

                # 5. LÓGICA TABÚ Y CRITERIO DE ASPIRACIÓN
                es_tabu = movimiento in lista_tabu
                # Criterio de Aspiración: permitimos un movimiento tabú si mejora
                # nuestra mejor solución encontrada hasta ahora.
                cumple_aspiracion = conflictos_actuales < mejor_conflictos

                if (not es_tabu or cumple_aspiracion) and conflictos_actuales < mejor_vecino_conflictos:
                    # Encontramos un nuevo mejor movimiento para esta iteración.
                    mejor_vecino_conflictos = conflictos_actuales
                    mejor_movimiento = (col, nueva_fila)
                
            # Restaura el tablero a su estado original para el siguiente ciclo.
            tablero_actual[col] = fila_original
        
        # 6. REALIZAR EL MEJOR MOVIMIENTO
        if mejor_movimiento:
            col, nueva_fila = mejor_movimiento
            tablero_actual[col] = nueva_fila # Moverse al nuevo estado.
            lista_tabu.append(mejor_movimiento) # Prohibir este movimiento por un tiempo.

            # Actualizar el mejor global si es necesario.
            if mejor_vecino_conflictos < mejor_conflictos:
                mejor_conflictos = mejor_vecino_conflictos
                mejor_tablero = list(tablero_actual)

    return mejor_tablero, mejor_conflictos

# --- Ejecución ---
SOLUCION_OPT = 0
TAMANO_TABLERO = 8
print(f"Buscando solución para {TAMANO_TABLERO}-Reinas con Búsqueda Tabú...")

resultado_tablero, conflictos_finales = resolver_n_reinas_tabu(n=TAMANO_TABLERO)

print("-" * 50)
print("Resultado Final (Mejor Configuración Encontrada):")
print(f"  Tablero: {resultado_tablero}")
print(f"  Conflictos: {conflictos_finales}")

if conflictos_finales == SOLUCION_OPT:
    print("✅ ¡Éxito! Se encontró una solución óptima sin conflictos.")
else:
    print("❌ La búsqueda finalizó sin encontrar la solución óptima.")