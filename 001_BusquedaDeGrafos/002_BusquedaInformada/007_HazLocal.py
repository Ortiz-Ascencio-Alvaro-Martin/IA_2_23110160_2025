# =========================================================================
# Búsqueda de Haz Local Simplificada para N-Reinas
# Objetivo: Minimizar el número de ataques a 0.
# =========================================================================

import random
import heapq

def contar_conflictos(tablero):
    """
    Función de costo simple: cuenta el número de pares de reinas que se atacan
    en las diagonales. El objetivo es alcanzar un costo de 0.
    """
    conflictos = 0
    n = len(tablero)
    for i in range(n):
        for j in range(i + 1, n):
            # Si la distancia horizontal es igual a la distancia vertical, hay un ataque.
            if abs(i - j) == abs(tablero[i] - tablero[j]):
                conflictos += 1
    return conflictos

def resolver_con_haz_local(n=8, tamano_haz=10, max_iter=100):
    """
    Implementa la Búsqueda de Haz Local manteniendo 'k' (tamano_haz) estados
    prometedores en cada iteración.
    """
    
    # 1. INICIALIZACIÓN: Crear un "haz" de 'k' estados iniciales aleatorios.
    haz = [tuple(random.randint(0, n - 1) for _ in range(n)) for _ in range(tamano_haz)]
    
    # Se guarda el mejor estado encontrado globalmente.
    mejor_estado_global = None
    mejor_costo_global = float('inf')

    # 2. BUCLE PRINCIPAL DE BÚSQUEDA
    for iteracion in range(max_iter):
        
        # 3. GENERAR SUCESORES DE TODO EL HAZ
        # Usamos un heap para mantener eficientemente los mejores candidatos.
        todos_los_sucesores = []
        
        for estado_actual in haz:
            # Actualizar el mejor estado global si encontramos uno mejor en el haz actual.
            costo_actual = contar_conflictos(estado_actual)
            if costo_actual < mejor_costo_global:
                mejor_costo_global = costo_actual
                mejor_estado_global = estado_actual
            
            # Si ya encontramos la solución, terminamos.
            if mejor_costo_global == 0:
                return mejor_estado_global, mejor_costo_global

            # Generar todos los vecinos del estado actual.
            for col in range(n):
                for fila in range(n):
                    if estado_actual[col] != fila:
                        vecino = list(estado_actual)
                        vecino[col] = fila
                        costo_vecino = contar_conflictos(vecino)
                        # Usamos heapq para mantener una lista de los mejores 'k' sucesores.
                        heapq.heappush(todos_los_sucesores, (costo_vecino, tuple(vecino)))

        # 4. SELECCIONAR EL NUEVO HAZ
        # El nuevo haz estará compuesto por los 'k' mejores sucesores únicos de la generación anterior.
        nuevo_haz = set()
        while todos_los_sucesores and len(nuevo_haz) < tamano_haz:
            # Extraemos el mejor sucesor (menor costo) del heap.
            costo, sucesor = heapq.heappop(todos_los_sucesores)
            nuevo_haz.add(sucesor)
        
        if not nuevo_haz:
            # Si no hay sucesores, la búsqueda termina.
            break
            
        haz = list(nuevo_haz)
        print(f"Iteración {iteracion + 1}: Mejor costo global = {mejor_costo_global}, Tamaño del haz = {len(haz)}")

    return mejor_estado_global, mejor_costo_global

# --- Ejecución del Algoritmo ---
SOLUCION_OPT = 0
TAMANO_TABLERO = 8

print(f"Problema: {TAMANO_TABLERO}-Reinas. Objetivo de Conflictos: {SOLUCION_OPT}")
resultado_tablero, conflictos_finales = resolver_con_haz_local(n=TAMANO_TABLERO, tamano_haz=10)

print("-" * 50)
print("Resultado Final (Búsqueda de Haz Local):")
print(f"  Mejor Tablero: {resultado_tablero}")
print(f"  Conflictos: {conflictos_finales}")

if conflictos_finales == SOLUCION_OPT:
    print("✅ ¡Éxito! Se encontró una solución óptima sin conflictos.")
else:
    print("❌ La búsqueda finalizó sin encontrar la solución óptima.")