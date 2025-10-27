# =========================================================================
# Red de Decisión Simple - Versión Simplificada
# Problema: ¿Debería llevar un paraguas?
# =========================================================================

# --- 1. Definición Unificada del Problema ---
# Se agrupan todas las partes de la red en una sola estructura de datos.
PROBLEMA_PARAGUAS = {
    # Cada acción tiene anidados sus posibles resultados y la utilidad de cada uno.
    'acciones': {
        'Llevar Paraguas': {
            'Lluvia': 50,  # Utilidad si llueve
            'Sol': 10      # Utilidad si hace sol
        },
        'No Llevar Paraguas': {
            'Lluvia': -100,
            'Sol': 80
        }
    },
    # Las probabilidades de los eventos inciertos (el clima).
    'probabilidades_estado': {
        'Lluvia': 0.4,
        'Sol': 0.6
    }
}

# --- 2. Algoritmo de Decisión (Más Directo) ---
def tomar_mejor_decision(problema):
    """
    Calcula la utilidad esperada para cada acción y elige la mejor.
    """
    utilidades_esperadas = {}
    
    # Itera sobre cada posible acción definida en el problema.
    for accion, resultados_accion in problema['acciones'].items():
        
        # Cálculo de la Utilidad Esperada (EU) de forma compacta.
        # EU = Suma de [ P(estado) * U(accion, estado) ]
        eu_calculada = sum(
            problema['probabilidades_estado'][estado] * utilidad
            for estado, utilidad in resultados_accion.items()
        )
        utilidades_esperadas[accion] = eu_calculada

    # Se encuentra la acción con la máxima utilidad esperada (MEU).
    mejor_accion = max(utilidades_esperadas, key=utilidades_esperadas.get)
    meu = utilidades_esperadas[mejor_accion]
    
    return mejor_accion, meu, utilidades_esperadas

# --- 3. Ejecución y Resultados ---
print("--- Análisis de Decisión: Paraguas ---")
mejor_opcion, max_utilidad, todas_las_eu = tomar_mejor_decision(PROBLEMA_PARAGUAS)

print("\nUtilidades Esperadas (EU) por Acción:")
for accion, eu in todas_las_eu.items():
    print(f"  - EU({accion}): {eu:.2f}")

print("\n--- Decisión Óptima (Principio de MEU) ---")
print(f"La acción recomendada es: '{mejor_opcion}'")
print(f"Máxima Utilidad Esperada (MEU): {max_utilidad:.2f}")