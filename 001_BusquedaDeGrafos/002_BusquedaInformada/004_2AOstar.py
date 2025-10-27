# =========================================================================
# Planificador de Tareas AND/OR (Concepto Modular de AO*)
# =========================================================================

def evaluar_opcion_exclusiva(opciones_or, estimaciones_h):
    """
    Evalúa un conjunto de opciones 'OR'. Encuentra la opción individual
    con el menor costo combinado (costo de la acción + heurística del sucesor).
    Retorna el costo y el subproblema de la mejor opción.
    """
    if not opciones_or:
        return float('inf'), None

    # Se calcula el costo estimado para cada opción y se busca la mejor.
    costos_calculados = [
        (costo_accion + estimaciones_h.get(sucesor, float('inf')), sucesor)
        for sucesor, costo_accion in opciones_or
    ]
    
    # min() elegirá la tupla con el primer elemento (costo) más bajo.
    mejor_costo, mejor_subproblema = min(costos_calculados)
    return mejor_costo, [mejor_subproblema] # Se devuelve como lista para consistencia.

def evaluar_opcion_conjunta(opciones_and, estimaciones_h):
    """
    Evalúa un conjunto de opciones 'AND'. El costo es la SUMA de los costos
    de todas las acciones y las heurísticas de todos los subproblemas.
    Retorna el costo total y la lista de todos los subproblemas a resolver.
    """
    if not opciones_and:
        return float('inf'), []

    costo_total = 0
    subproblemas_requeridos = []

    for sucesor, costo_accion in opciones_and:
        # Se acumula el costo de cada sub-tarea.
        costo_total += costo_accion + estimaciones_h.get(sucesor, float('inf'))
        subproblemas_requeridos.append(sucesor)
        
    return costo_total, subproblemas_requeridos

def determinar_mejor_estrategia(problema, grafo_descomposicion, estimaciones_h):
    """
    Función principal que simula la decisión de AO*.
    Compara el costo de la mejor opción 'OR' contra el costo total 'AND'.
    """
    # 1. Obtiene las posibles descomposiciones del problema actual.
    descomposiciones = grafo_descomposicion.get(problema, {})
    
    # 2. Evalúa las dos posibles estrategias por separado.
    costo_or, plan_or = evaluar_opcion_exclusiva(descomposiciones.get('OR', []), estimaciones_h)
    costo_and, plan_and = evaluar_opcion_conjunta(descomposiciones.get('AND', []), estimaciones_h)
    
    # 3. Compara los resultados y elige la estrategia de menor costo.
    if costo_or <= costo_and:
        return {
            "estrategia": "OR",
            "costo_estimado": costo_or,
            "subproblemas": plan_or
        }
    else:
        return {
            "estrategia": "AND",
            "costo_estimado": costo_and,
            "subproblemas": plan_and
        }

# --- Datos del Problema ---
AND_OR_GRAFO = {
    'P1': {'OR': [('P2', 1)], 'AND': [('P3', 2), ('P4', 2)]},
    'P2': {'OR': [('RESUELTO', 0)]},
    'P3': {'OR': [('RESUELTO', 0)]},
    'P4': {'OR': [('RESUELTO', 0)]},
    'RESUELTO': {}
}

heuristica_ao = {
    'P1': 10, 'P2': 5, 'P3': 3, 'P4': 4, 'RESUELTO': 0
}

INICIO = 'P1'

print("Grafo AND/OR (Descomposiciones):")
for nodo, ramas in AND_OR_GRAFO.items():
    print(f"  {nodo}: {ramas}")
print(f"Heurística h(n): {heuristica_ao}")
print("-" * 50)

# --- Ejecución del Algoritmo ---
plan_optimo = determinar_mejor_estrategia(INICIO, AND_OR_GRAFO, heuristica_ao)

print(f"Evaluando el problema inicial '{INICIO}':")
print(f"  Costo estimado vía OR (P2): 1 (costo) + 5 (h(P2)) = 6")
print(f"  Costo estimado vía AND (P3, P4): [2+3] + [2+4] = 11")
print("-" * 50)
print("Resultado AO* (Mejor Estrategia):")
print(f"  - Decisión Óptima: Elegir la estrategia '{plan_optimo['estrategia']}'")
print(f"  - Subproblemas a resolver: {plan_optimo['subproblemas']}")
print(f"  - Costo Total Estimado: {plan_optimo['costo_estimado']}")