# =========================================================================
# Solucionador de CSP con Comprobación Hacia Delante (Forward Checking)
# Implementación Procedural con Restauración de Dominios
# =========================================================================

# --- 1. DEFINICIÓN DEL PROBLEMA (Planificación de Tareas) ---
TAREAS = ['T1', 'T2', 'T3']
HORARIOS_INICIALES = {
    'T1': ['L', 'M', 'X'],
    'T2': ['L', 'M', 'X'],
    'T3': ['L', 'M', 'X']
}
# Las restricciones indican qué tareas no pueden ocurrir al mismo tiempo.
CONFLICTOS = [('T1', 'T2'), ('T1', 'T3'), ('T2', 'T3')]

# --- 2. LÓGICA DEL ALGORITMO ---

def obtener_vecinos(tarea, conflictos):
    """Función auxiliar para encontrar los vecinos de una tarea."""
    vecinos = []
    for t1, t2 in conflictos:
        if t1 == tarea:
            vecinos.append(t2)
        elif t2 == tarea:
            vecinos.append(t1)
    return vecinos

def aplicar_forward_checking(tarea, horario, dominios):
    """
    Poda los dominios de los vecinos. En lugar de retornar True/False,
    retorna una lista de los cambios realizados ("podas") para poder revertirlos.
    Si la poda falla (un dominio queda vacío), retorna None.
    """
    podas_realizadas = []
    
    for vecino in obtener_vecinos(tarea, CONFLICTOS):
        if horario in dominios[vecino]:
            # Se elimina el horario del dominio del vecino.
            dominios[vecino].remove(horario)
            # Se registra el cambio para poder deshacerlo después.
            podas_realizadas.append((vecino, horario))
            
            # Fallo temprano: si un vecino se queda sin opciones, esta ruta no es válida.
            if not dominios[vecino]:
                # Antes de fallar, se deshacen las podas hechas en ESTA llamada.
                for v, h in podas_realizadas:
                    dominios[v].append(h)
                return None # Indica fallo.
                
    return podas_realizadas # Indica éxito y devuelve los cambios.

def restaurar_dominios(dominios, podas):
    """
    Revierte los cambios hechos por el forward checking. Es el paso clave
    en el backtracking manual de dominios.
    """
    for tarea, horario in podas:
        dominios[tarea].append(horario)

def encontrar_horario(asignacion, dominios):
    """
    El motor recursivo del algoritmo de backtracking.
    """
    # Caso Base: Si todas las tareas tienen horario, hemos encontrado una solución.
    if len(asignacion) == len(TAREAS):
        return asignacion

    # 1. Seleccionar la siguiente tarea sin horario.
    tarea_actual = next(t for t in TAREAS if t not in asignacion)
    
    # 2. Iterar sobre los horarios disponibles para esa tarea.
    #    Se itera sobre una copia para no tener problemas al modificar la lista original.
    for horario in list(dominios[tarea_actual]):
        
        # 3. Aplicar Comprobación Hacia Delante.
        podas = aplicar_forward_checking(tarea_actual, horario, dominios)
        
        # Si 'podas' no es None, la poda fue exitosa.
        if podas is not None:
            
            # Se aplica la asignación.
            asignacion[tarea_actual] = horario
            
            # Se continúa con la siguiente tarea.
            resultado = encontrar_horario(asignacion, dominios)
            
            if resultado:
                return resultado # ¡Solución encontrada!
            
            # --- 4. VUELTA ATRÁS (BACKTRACK) ---
            # Si la recursión no encontró solución, deshacer los cambios.
            del asignacion[tarea_actual]
            restaurar_dominios(dominios, podas) # <- Clave: se revierten las podas.

    # Si se probaron todos los horarios y ninguno funcionó, esta rama falla.
    return None

# --- 3. EJECUCIÓN ---
# El algoritmo necesita una copia de los dominios para modificarla.
dominios_de_trabajo = {t: list(h) for t, h in HORARIOS_INICIALES.items()}
print("Buscando un horario válido con Backtracking y Forward Checking...")

solucion = encontrar_horario({}, dominios_de_trabajo)

print("-" * 50)
if solucion:
    print("Horario válido encontrado.")
    print(f"   Asignaciones finales: {solucion}")
else:
    print("No se encontró una solución compatible.")
    #