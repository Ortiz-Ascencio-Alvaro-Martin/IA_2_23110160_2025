# =========================================================================
# Solucionador de CSP con Comprobación Hacia Delante (Forward Checking)
# Implementación Orientada a Objetos
# =========================================================================

import copy

class SolucionadorCSP_FC:
    """
    Encapsula un problema CSP y lo resuelve usando backtracking con la
    optimización de Comprobación Hacia Delante (Forward Checking).
    """

    def __init__(self, variables, dominios, restricciones):
        """
        Inicializa el problema y convierte las restricciones a un formato
        de acceso rápido (diccionario de vecinos).
        """
        self.variables = variables
        self.dominios_iniciales = dominios
        self.vecinos = self._convertir_restricciones(restricciones)
        print("🔎 Solucionador CSP con Forward Checking inicializado.")

    def _convertir_restricciones(self, restricciones):
        """Convierte una lista de pares en un diccionario de vecinos."""
        vecinos = {v: [] for v in self.variables}
        for v1, v2 in restricciones:
            vecinos[v1].append(v2)
            vecinos[v2].append(v1)
        return vecinos

    def _forward_check(self, variable, valor, dominios):
        """
        Realiza la "poda" de dominios. Después de asignar 'valor' a 'variable',
        elimina ese valor de los dominios de todos sus vecinos.
        Retorna True si la poda es exitosa, False si algún dominio queda vacío.
        """
        for vecino in self.vecinos[variable]:
            if valor in dominios[vecino]:
                dominios[vecino].remove(valor)
                # Fallo temprano: si un vecino se queda sin opciones, esta ruta no es válida.
                if not dominios[vecino]:
                    return False
        return True

    def _backtrack_con_fc(self, asignacion, dominios):
        """
        El motor recursivo del algoritmo.
        """
        # Caso Base: Si la asignación está completa, hemos encontrado una solución.
        if len(asignacion) == len(self.variables):
            return asignacion

        # 1. Seleccionar la siguiente variable sin asignar.
        variable_actual = next(v for v in self.variables if v not in asignacion)

        # 2. Iterar sobre los valores del dominio actual para esa variable.
        for valor in dominios[variable_actual]:
            
            # 3. Preparar la siguiente recursión creando copias.
            #    Esto simplifica enormemente el backtracking.
            nueva_asignacion = asignacion.copy()
            nueva_asignacion[variable_actual] = valor
            
            dominios_copiados = copy.deepcopy(dominios)
            
            # 4. Aplicar Comprobación Hacia Delante.
            if self._forward_check(variable_actual, valor, dominios_copiados):
                
                # Si la poda fue exitosa, continuar con la siguiente variable.
                resultado = self._backtrack_con_fc(nueva_asignacion, dominios_copiados)
                
                # Si se encontró una solución, propagarla hacia arriba.
                if resultado:
                    return resultado
        
        # Si se probaron todos los valores y ninguno llevó a una solución, esta rama falla.
        return None

    def resolver(self):
        """
        Punto de entrada público para iniciar el proceso de solución.
        """
        print("Iniciando búsqueda con Comprobación Hacia Delante...")
        # Inicia la recursión con una asignación vacía y una copia de los dominios iniciales.
        return self._backtrack_con_fc({}, copy.deepcopy(self.dominios_iniciales))

# --- 1. DEFINICIÓN DEL PROBLEMA ---
VARIABLES_CSP = ['T1', 'T2', 'T3']
DOMINIOS_CSP = {
    'T1': ['L', 'M', 'X'],
    'T2': ['L', 'M', 'X'],
    'T3': ['L', 'M', 'X']
}
RESTRICCIONES_CSP = [('T1', 'T2'), ('T1', 'T3'), ('T2', 'T3')]

# --- 2. EJECUCIÓN ---
# Se crea una instancia del solucionador con la definición del problema.
mi_csp_fc = SolucionadorCSP_FC(VARIABLES_CSP, DOMINIOS_CSP, RESTRICCIONES_CSP)

# Se llama al método para resolverlo.
solucion = mi_csp_fc.resolver()

# --- 3. RESULTADOS ---
print("-" * 50)
if solucion:
    print(" ¡Solución encontrada!")
    print(f"   Asignaciones finales: {solucion}")
else:
    print(" No se encontró una solución para este problema.")