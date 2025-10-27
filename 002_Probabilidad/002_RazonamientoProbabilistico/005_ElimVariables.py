# =========================================================================
# Inferencia en Redes Bayesianas con Eliminación de Variables (Versión OOP)
# =========================================================================

import itertools
import copy

class Factor:
    """Representa un factor en una red bayesiana, definido por un conjunto de
    variables y una tabla de probabilidad condicional (CPT)."""
    def __init__(self, variables, cpt):
        self.variables = tuple(variables)
        self.cpt = cpt

    def __repr__(self):
        return f"Factor({self.variables})"

def multiply_factors(factor1, factor2):
    """Multiplica dos factores para crear uno nuevo."""
    # Encontrar variables comunes y el nuevo conjunto de variables.
    vars1 = set(factor1.variables)
    vars2 = set(factor2.variables)
    new_vars = tuple(sorted(list(vars1.union(vars2))))
    new_cpt = {}

    # Generar todas las asignaciones posibles para las nuevas variables.
    var_domains = {var: set() for var in new_vars}
    for assignment in factor1.cpt.keys():
        for i, var in enumerate(factor1.variables):
            var_domains[var].add(assignment[i])
    for assignment in factor2.cpt.keys():
        for i, var in enumerate(factor2.variables):
            var_domains[var].add(assignment[i])
    
    assignments = itertools.product(*(var_domains[var] for var in new_vars))

    for assignment in assignments:
        # Extraer las asignaciones para cada factor original y multiplicar.
        assignment_dict = {var: val for var, val in zip(new_vars, assignment)}
        key1 = tuple(assignment_dict[var] for var in factor1.variables)
        key2 = tuple(assignment_dict[var] for var in factor2.variables)
        
        prob1 = factor1.cpt.get(key1, 0)
        prob2 = factor2.cpt.get(key2, 0)
        new_cpt[assignment] = prob1 * prob2
        
    return Factor(new_vars, new_cpt)

def sum_out(factor, variable):
    """Elimina una variable de un factor por marginalización (suma)."""
    if variable not in factor.variables:
        return factor

    new_vars = tuple(v for v in factor.variables if v != variable)
    var_index = factor.variables.index(variable)
    new_cpt = {}

    for assignment in factor.cpt:
        new_key = assignment[:var_index] + assignment[var_index+1:]
        new_cpt[new_key] = new_cpt.get(new_key, 0) + factor.cpt[assignment]
        
    return Factor(new_vars, new_cpt)

class VariableEliminationSolver:
    def __init__(self, factors):
        self.factors = factors

    def infer(self, query_var, evidence, elimination_order):
        """
        Realiza inferencia usando el algoritmo de Eliminación de Variables.
        """
        # 1. Aplicar la evidencia: reducir los factores.
        working_factors = []
        for f in self.factors:
            new_cpt = {}
            for assignment, prob in f.cpt.items():
                is_consistent = True
                for i, var in enumerate(f.variables):
                    if var in evidence and evidence[var] != assignment[i]:
                        is_consistent = False
                        break
                if is_consistent:
                    new_cpt[assignment] = prob
            working_factors.append(Factor(f.variables, new_cpt))
            
        # 2. Eliminar las variables una por una.
        for var_to_eliminate in elimination_order:
            factors_with_var = [f for f in working_factors if var_to_eliminate in f.variables]
            working_factors = [f for f in working_factors if var_to_eliminate not in f.variables]
            
            # Multiplicar todos los factores que contienen la variable.
            product_factor = factors_with_var[0]
            for i in range(1, len(factors_with_var)):
                product_factor = multiply_factors(product_factor, factors_with_var[i])
            
            # Eliminar la variable del factor resultante.
            new_factor = sum_out(product_factor, var_to_eliminate)
            working_factors.append(new_factor)

        # 3. Multiplicar los factores restantes y normalizar.
        final_factor = working_factors[0]
        for i in range(1, len(working_factors)):
            final_factor = multiply_factors(final_factor, working_factors[i])
        
        # Normalización
        total = sum(final_factor.cpt.values())
        return {key[0]: val / total for key, val in final_factor.cpt.items()}

# --- 1. DEFINICIÓN DEL MODELO COMO FACTORES ---
factors = [
    Factor(('D',), {('Alta',): 0.6, ('Baja',): 0.4}),
    Factor(('I',), {('Alta',): 0.7, ('Baja',): 0.3}),
    Factor(('I', 'L'), {('Alta', 'Fuerte'): 0.8, ('Alta', 'Débil'): 0.2, ('Baja', 'Fuerte'): 0.3, ('Baja', 'Débil'): 0.7}),
    Factor(('D', 'I', 'G'), {
        ('Alta', 'Alta', 'A'): 0.3, ('Alta', 'Alta', 'B'): 0.7,
        ('Alta', 'Baja', 'A'): 0.05, ('Alta', 'Baja', 'B'): 0.95,
        ('Baja', 'Alta', 'A'): 0.9, ('Baja', 'Alta', 'B'): 0.1,
        ('Baja', 'Baja', 'A'): 0.5, ('Baja', 'Baja', 'B'): 0.5
    })
]

# --- 2. EJECUCIÓN DE LA INFERENCIA ---
solver = VariableEliminationSolver(factors)
resultado = solver.infer(
    query_var='L',
    evidence={'G': 'A'},
    elimination_order=['D', 'I']
)

# --- 3. RESULTADOS ---
print("--- Inferencia con Eliminación de Variables (Generalizada) ---")
print("Consulta: P(L | G='A'), Orden de Eliminación: ['D', 'I']")
print("-" * 60)
print("Resultado Final de la Inferencia:")
for valor, prob in resultado.items():
    print(f"  P(L={valor} | G='A') = {prob:.4f}")