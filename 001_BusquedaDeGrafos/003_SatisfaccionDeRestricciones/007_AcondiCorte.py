# =========================================================================
# Acondicionamiento del Corte (Cutset Conditioning) - Versión Orientada a Objetos
# Problema: Colorear un mapa cíclico de 4 regiones.
# =========================================================================

import itertools

class CutsetSolver:
    """
    Encapsula la lógica para resolver un CSP usando Acondicionamiento del Corte.
    La idea es "condicionar" (fijar) un conjunto de variables (el corte) que,
    al ser eliminadas, convierten el problema en una estructura de árbol fácil de resolver.
    """

    def __init__(self, variables, dominio, restricciones, corte):
        self.variables = variables
        self.dominio = dominio
        self.corte = corte
        
        # 1. Separar las variables del corte de las restantes (el "árbol").
        self.variables_arbol = [v for v in variables if v not in corte]
        
        # 2. Crear un mapa de vecinos para comprobaciones rápidas.
        self.vecinos = {v: [] for v in variables}
        for v1, v2 in restricciones:
            self.vecinos[v1].append(v2)
            self.vecinos[v2].append(v1)

    def _es_consistente(self, variable, valor, asignacion):
        """Verifica si una nueva asignación es válida con las ya existentes."""
        for vecino in self.vecinos[variable]:
            if vecino in asignacion and asignacion[vecino] == valor:
                return False
        return True

    def _resolver_arbol_restante(self, asignacion):
        """
        Un solucionador de backtracking simple que opera solo sobre las variables
        del "árbol", ya que el corte ya está fijado.
        """
        # Caso base: si todas las variables (corte + árbol) están asignadas, es una solución.
        if len(asignacion) == len(self.variables):
            return asignacion

        # Seleccionar la siguiente variable del árbol para asignar.
        variable_a_asignar = next(v for v in self.variables_arbol if v not in asignacion)

        for valor in self.dominio:
            if self._es_consistente(variable_a_asignar, valor, asignacion):
                asignacion[variable_a_asignar] = valor
                resultado = self._resolver_arbol_restante(asignacion)
                if resultado:
                    return resultado
                # Vuelta atrás (Backtrack)
                del asignacion[variable_a_asignar]
        
        return None

    def resolver(self):
        """
        Punto de entrada principal. Itera sobre las asignaciones del corte y
        trata de resolver el subproblema para cada una.
        """
        # 3. Generar todas las posibles asignaciones para las variables del corte.
        posibles_valores_corte = itertools.product(self.dominio, repeat=len(self.corte))

        for valores_corte in posibles_valores_corte:
            asignacion_inicial = {var: val for var, val in zip(self.corte, valores_corte)}
            
            print(f"\nIntentando con la asignación del corte: {asignacion_inicial}")

            # 4. Para cada asignación del corte, intentar resolver el problema restante.
            solucion = self._resolver_arbol_restante(asignacion_inicial)

            # 5. Si se encuentra una solución, el problema está resuelto.
            if solucion:
                print("  -> Solución encontrada para el subproblema.")
                return solucion
            else:
                print("  -> Esta asignación del corte no permite una solución.")
        
        return None

# --- 1. DEFINICIÓN DEL PROBLEMA ---
REGIONES = ['Norte', 'Este', 'Sur', 'Oeste']
COLORES = [1, 2]
VECINOS = [('Norte', 'Este'), ('Este', 'Sur'), ('Sur', 'Oeste'), ('Oeste', 'Norte')]

# El CORTE: Al fijar 'Norte', el resto ('Este'-'Sur'-'Oeste') es una línea simple.
CORTE_W = ['Norte']

# --- 2. EJECUCIÓN ---
solucionador = CutsetSolver(REGIONES, COLORES, VECINOS, CORTE_W)
solucion_final = solucionador.resolver()

print("\n" + "="*50)
if solucion_final:
    print("¡Solución Encontrada!")
    print(f"  Asignaciones: {solucion_final}")
else:
    print("No se encontró ninguna solución.")
    #