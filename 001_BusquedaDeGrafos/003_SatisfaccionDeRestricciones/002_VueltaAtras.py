# =========================================================================
# Solucionador de Problemas de Satisfacción de Restricciones (CSP)
# Implementación Orientada a Objetos del Backtracking
# =========================================================================

class SolucionadorCSP:
    """
    Encapsula un problema CSP (variables, dominios, restricciones) y lo
    resuelve usando un algoritmo de backtracking recursivo.
    """

    def __init__(self, variables, dominios, restricciones):
        """
        Inicializa el problema con sus componentes.
        """
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
        print("🔎 Solucionador CSP inicializado.")

    def _es_consistente(self, variable, valor, asignacion):
        """
        Verifica si una asignación parcial sigue siendo válida al añadir
        un nuevo par (variable, valor).
        """
        # Itera sobre todas las restricciones definidas para el problema.
        for v1, v2 in self.restricciones:
            # Comprueba si la restricción involucra a la variable actual.
            if v1 == variable and v2 in asignacion and valor == asignacion[v2]:
                return False  # Conflicto encontrado
            if v2 == variable and v1 in asignacion and valor == asignacion[v1]:
                return False  # Conflicto encontrado
        return True # La asignación no viola ninguna restricción.

    def _backtrack(self, asignacion):
        """
        El motor recursivo del algoritmo de backtracking.
        """
        # Caso Base: Si la asignación está completa, hemos encontrado una solución.
        if len(asignacion) == len(self.variables):
            return asignacion

        # 1. Seleccionar la siguiente variable a la que se le asignará un valor.
        variable_actual = next(v for v in self.variables if v not in asignacion)

        # 2. Iterar sobre todos los posibles valores para la variable actual.
        for valor in self.dominios[variable_actual]:
            
            # 3. Comprobar si la asignación es consistente con las reglas.
            if self._es_consistente(variable_actual, valor, asignacion):
                
                # Si es consistente, se aplica la asignación.
                asignacion[variable_actual] = valor
                
                # Se llama recursivamente para continuar con la siguiente variable.
                resultado = self._backtrack(asignacion)
                
                # Si la llamada recursiva encontró una solución, se propaga hacia arriba.
                if resultado:
                    return resultado
                
                # 4. Vuelta Atrás (Backtrack): Si no, se deshace la asignación para probar
                #    el siguiente valor. Este es el paso clave del algoritmo.
                del asignacion[variable_actual]

        # Si se probaron todos los valores y ninguno funcionó, esta rama no tiene solución.
        return None

    def resolver(self):
        """
        Punto de entrada público para iniciar el proceso de solución.
        """
        print("Iniciando búsqueda de una solución...")
        return self._backtrack({})

# --- 1. DEFINICIÓN DEL PROBLEMA ---
VARIABLES_CSP = ['A', 'B', 'C']
DOMINIOS_CSP = {
    'A': ['Rojo', 'Verde'],
    'B': ['Rojo', 'Verde'],
    'C': ['Rojo', 'Verde']
}
RESTRICCIONES_CSP = [('A', 'B'), ('A', 'C')]

# --- 2. EJECUCIÓN ---
# Se crea una instancia del solucionador con la definición del problema.
mi_csp = SolucionadorCSP(VARIABLES_CSP, DOMINIOS_CSP, RESTRICCIONES_CSP)

# Se llama al método para resolverlo.
solucion = mi_csp.resolver()

# --- 3. RESULTADOS ---
print("-" * 50)
if solucion:
    print(" ¡Solución encontrada!")
    print(f"   Asignaciones finales: {solucion}")
else:
    print(" No se encontró una solución para este problema.")