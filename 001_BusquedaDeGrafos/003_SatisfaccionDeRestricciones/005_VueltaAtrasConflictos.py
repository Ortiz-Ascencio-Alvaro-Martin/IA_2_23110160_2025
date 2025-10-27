# =========================================================================
# Salto Atrás Dirigido por Conflictos (CBJ) - Implementación Funcional
# Problema: Asignar horarios a tareas con restricciones.
# =========================================================================

# --- 1. DEFINICIÓN DEL PROBLEMA ---
TAREAS = ['T1', 'T2', 'T3', 'T4']
HORARIOS = [1, 2, 3]

# Reglas: indican qué tareas entran en conflicto con otras.
# T4 entra en conflicto con T1 y T3.
REGLAS_DE_CONFLICTO = {
    'T4': ['T1', 'T3']
}

# --- 2. LÓGICA DEL ALGORITMO ---

def verificar_conflicto(tarea, horario, asignacion):
    """
    Verifica si asignar un 'horario' a una 'tarea' causa un conflicto.
    Si lo hace, retorna el CONJUNTO de variables ya asignadas que causan el problema.
    """
    conjunto_conflicto = set()
    # Busca las tareas que restringen a la tarea actual.
    for tarea_restrictiva in REGLAS_DE_CONFLICTO.get(tarea, []):
        # Si la tarea restrictiva ya tiene un horario y es el mismo, hay conflicto.
        if tarea_restrictiva in asignacion and asignacion[tarea_restrictiva] == horario:
            conjunto_conflicto.add(tarea_restrictiva)
    return conjunto_conflicto

def resolver_con_salto_dirigido(asignacion):
    """
    Motor recursivo de backtracking que incorpora la lógica de CBJ.
    Retorna dos valores: la solución (o None) y el conjunto de conflicto.
    """
    # Caso Base: Si todas las tareas están asignadas, encontramos una solución.
    if len(asignacion) == len(TAREAS):
        return asignacion, set()

    tarea_actual = next(t for t in TAREAS if t not in asignacion)
    conflicto_acumulado = set()

    for horario in HORARIOS:
        # 1. Verificar si el horario actual causa un conflicto.
        conflicto_directo = verificar_conflicto(tarea_actual, horario, asignacion)

        if not conflicto_directo:
            # Si no hay conflicto directo, se asigna y se avanza.
            asignacion[tarea_actual] = horario
            
            # Llamada recursiva para la siguiente tarea.
            resultado, conflicto_heredado = resolver_con_salto_dirigido(asignacion)
            
            # Si se encontró una solución, se propaga hacia arriba.
            if resultado:
                return resultado, set()

            # 2. LÓGICA CLAVE DE CBJ: Analizar el conflicto heredado.
            # Si la tarea actual NO es parte del conflicto de una rama futura,
            # significa que cambiar su valor no resolverá el problema.
            if tarea_actual not in conflicto_heredado:
                # Se deshace la asignación y se "salta" inmediatamente.
                del asignacion[tarea_actual]
                # Se pasa el conflicto heredado intacto al nivel anterior.
                return None, conflicto_heredado
            
            # Si la tarea actual SÍ es parte del conflicto, se acumula y se intenta otro horario.
            conflicto_acumulado.update(conflicto_heredado - {tarea_actual})
            del asignacion[tarea_actual]

        else:
            # Si hubo un conflicto directo, se acumulan las causas.
            conflicto_acumulado.update(conflicto_directo)
            
    # Si se probaron todos los horarios y ninguno funcionó, se retorna el conflicto acumulado.
    return None, conflicto_acumulado

# --- 3. EJECUCIÓN ---
print("Buscando una asignación válida con Salto Atrás Dirigido por Conflictos...")
solucion, _ = resolver_con_salto_dirigido({})

print("-" * 50)
if solucion:
    print("¡Solución encontrada!")
    print(f"  Asignaciones: {solucion}")
else:
    print("No se encontró una solución.")