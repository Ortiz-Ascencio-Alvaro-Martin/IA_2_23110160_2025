# =========================================================================
# Temple Simulado (Recocido Simulado) para N-Reinas - Versión Simplificada
# =========================================================================

import random
import math

def resolver_n_reinas_con_temple(n=8, temp_inicial=1.0, factor_enfriamiento=0.995):
    """
    Implementa el algoritmo de Temple Simulado de forma más compacta para el problema de las N-Reinas.
    El objetivo es encontrar una configuración con 0 conflictos.
    """
    
    # --- Función de Costo (Anidada para mantener todo junto) ---
    def calcular_conflictos(tablero):
        """Calcula el número de pares de reinas que se atacan en diagonal."""
        conflictos = 0
        largo = len(tablero)
        for i in range(largo):
            for j in range(i + 1, largo):
                if abs(i - j) == abs(tablero[i] - tablero[j]):
                    conflictos += 1
        return conflictos

    # 1. ESTADO INICIAL
    # Un tablero aleatorio donde el índice es la columna y el valor es la fila.
    estado_actual = [random.randint(0, n - 1) for _ in range(n)]
    costo_actual = calcular_conflictos(estado_actual)
    
    # Guardamos la mejor solución encontrada.
    mejor_estado = list(estado_actual)
    mejor_costo = costo_actual
    
    temperatura = temp_inicial
    
    print(f"Inicio: {estado_actual} (Conflictos: {costo_actual})")

    # 2. BUCLE DE ENFRIAMIENTO
    # El proceso continúa mientras el sistema tenga "energía" (temperatura).
    while temperatura > 1e-5 and mejor_costo > 0:
        
        # 3. GENERAR UN VECINO (un cambio pequeño y aleatorio)
        # Se elige una reina al azar y se mueve a una nueva fila al azar.
        vecino = list(estado_actual)
        col_a_mover = random.randint(0, n - 1)
        nueva_fila = random.randint(0, n - 1)
        vecino[col_a_mover] = nueva_fila
        costo_vecino = calcular_conflictos(vecino)
        
        # 4. DECIDIR SI ACEPTAR EL NUEVO ESTADO
        # Delta de costo: diferencia entre el costo nuevo y el viejo.
        delta_costo = costo_vecino - costo_actual
        
        # Si el vecino es mejor (delta < 0), la probabilidad es > 1, se acepta siempre.
        # Si el vecino es peor (delta > 0), se acepta con una probabilidad decreciente.
        # P = e^(-ΔCosto / T)
        if random.random() < math.exp(-delta_costo / temperatura):
            estado_actual = vecino
            costo_actual = costo_vecino
            
            # Si este nuevo estado es el mejor que hemos visto, se guarda.
            if costo_actual < mejor_costo:
                mejor_costo = costo_actual
                mejor_estado = list(estado_actual)
                
        # 5. ENFRIAR EL SISTEMA
        # Se reduce la temperatura, haciendo más difícil aceptar malos movimientos.
        temperatura *= factor_enfriamiento
        
    return mejor_estado, mejor_costo

# --- Ejecución del Algoritmo ---
SOLUCION_OPT = 0
TAMANO_TABLERO = 8

print(f"Buscando solución para {TAMANO_TABLERO}-Reinas con Temple Simulado...")

resultado_tablero, conflictos_finales = resolver_n_reinas_con_temple(n=TAMANO_TABLERO)

print("-" * 50)
print("Resultado Final (Mejor Configuración Encontrada):")
print(f"  Tablero: {resultado_tablero}")
print(f"  Conflictos: {conflictos_finales}")

if conflictos_finales == SOLUCION_OPT:
    print("✅ ¡Éxito! Se encontró una solución óptima sin conflictos.")
else:
    print("❌ La búsqueda finalizó (se enfrió) sin encontrar la solución óptima.")