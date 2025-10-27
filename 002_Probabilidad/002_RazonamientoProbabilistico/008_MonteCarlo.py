# =========================================================================
# Inferencia Aproximada con Muestreo de Gibbs (Versión OOP y Generalizada)
# =========================================================================

import random

class GibbsSampler:
    """
    Representa una Red Bayesiana y puede realizar inferencia aproximada
    utilizando el algoritmo de Muestreo de Gibbs (un método MCMC).
    """

    def __init__(self, red_bayesiana):
        """
        Inicializa el muestreador con la estructura y las CPTs de la red.
        """
        self.nodos = red_bayesiana['nodos']
        self.padres = red_bayesiana['padres']
        self.hijos = red_bayesiana['hijos']
        self.cpts = red_bayesiana['cpts']

    def _probabilidad_condicional(self, variable, valor, estado_actual):
        """
        Calcula la probabilidad de una variable dado su Manto de Markov.
        P(X | MB(X)) = α * P(X | Padres(X)) * Π P(Hijo_i | Padres(Hijo_i))
        """
        # 1. Término de los padres: P(Variable | Padres(Variable))
        padres_de_var = self.padres[variable]
        configuracion_padres = tuple(estado_actual[p] for p in padres_de_var)
        prob_dado_padres = self.cpts[variable][configuracion_padres][valor]

        # 2. Término de los hijos: Π P(Hijo_i | Padres(Hijo_i))
        prob_hijos = 1.0
        for hijo in self.hijos[variable]:
            # El estado actual ya contiene los valores de los otros padres del hijo.
            padres_del_hijo = self.padres[hijo]
            configuracion_padres_hijo = tuple(estado_actual[p] for p in padres_del_hijo)
            valor_hijo = estado_actual[hijo]
            prob_hijos *= self.cpts[hijo][configuracion_padres_hijo][valor_hijo]
            
        return prob_dado_padres * prob_hijos

    def inferir(self, var_consulta, evidencia, num_iteraciones, burn_in):
        """
        Estima la distribución P(Consulta | Evidencia) usando Muestreo de Gibbs.
        """
        # 1. Inicialización: Fijar la evidencia y asignar valores aleatorios al resto.
        estado_actual = evidencia.copy()
        variables_no_evidencia = [v for v in self.nodos if v not in evidencia]
        for var in variables_no_evidencia:
            estado_actual[var] = random.choice(self.cpts[var]['valores'])

        # 2. Contadores para los resultados después del "burn-in".
        conteo_resultados = {valor: 0 for valor in self.cpts[var_consulta]['valores']}

        # 3. Bucle de Muestreo (Cadena de Markov).
        for i in range(num_iteraciones):
            # Iterar sobre cada variable que no es evidencia.
            for var_a_muestrear in variables_no_evidencia:
                
                # a) Calcular la distribución condicional completa P(Var | Manto de Markov).
                distribucion = {}
                for valor_posible in self.cpts[var_a_muestrear]['valores']:
                    estado_temporal = estado_actual.copy()
                    estado_temporal[var_a_muestrear] = valor_posible
                    distribucion[valor_posible] = self._probabilidad_condicional(var_a_muestrear, valor_posible, estado_temporal)
                
                # b) Normalizar y muestrear un nuevo valor para la variable.
                total_prob = sum(distribucion.values())
                if total_prob > 0:
                    rand_val = random.random() * total_prob
                    cumulative_prob = 0.0
                    for valor, prob in distribucion.items():
                        cumulative_prob += prob
                        if rand_val < cumulative_prob:
                            estado_actual[var_a_muestrear] = valor
                            break
            
            # c) Acumular los resultados si ya pasó el período de "burn-in".
            if i >= burn_in:
                valor_actual_consulta = estado_actual[var_consulta]
                conteo_resultados[valor_actual_consulta] += 1
        
        # 4. Normalizar los conteos para obtener la distribución final.
        total_muestras_validas = sum(conteo_resultados.values())
        return {valor: conteo / total_muestras_validas for valor, conteo in conteo_resultados.items()}

# --- 1. DEFINICIÓN DEL MODELO DE LA RED ---
RED_ASPERSOR = {
    'nodos': ['Lluvia', 'Aspersor', 'Humedo'],
    'padres': {'Lluvia': [], 'Aspersor': [], 'Humedo': ['Lluvia', 'Aspersor']},
    'hijos': {'Lluvia': ['Humedo'], 'Aspersor': ['Humedo'], 'Humedo': []},
    'cpts': {
        'Lluvia': {'valores': ['Si', 'No'], (): {'Si': 0.2, 'No': 0.8}},
        'Aspersor': {'valores': ['Si', 'No'], (): {'Si': 0.1, 'No': 0.9}},
        'Humedo': {
            'valores': ['Si', 'No'],
            ('Si', 'Si'): {'Si': 0.99, 'No': 0.01}, ('Si', 'No'): {'Si': 0.90, 'No': 0.10},
            ('No', 'Si'): {'Si': 0.90, 'No': 0.10}, ('No', 'No'): {'Si': 0.01, 'No': 0.99}
        }
    }
}

# --- 2. CONFIGURACIÓN DE LA INFERENCIA ---
VARIABLE_CONSULTA = 'Lluvia'
EVIDENCIA = {'Humedo': 'Si'}
NUM_ITERACIONES = 50000
BURN_IN = 1000

# --- 3. EJECUCIÓN ---
muestreador_gibbs = GibbsSampler(RED_ASPERSOR)
resultado = muestreador_gibbs.inferir(VARIABLE_CONSULTA, EVIDENCIA, NUM_ITERACIONES, BURN_IN)

# --- 4. RESULTADOS ---
print(f"--- Inferencia MCMC con Muestreo de Gibbs ---")
print(f"Consulta: P({VARIABLE_CONSULTA} | {list(EVIDENCIA.keys())[0]}='{list(EVIDENCIA.values())[0]}')")
print(f"Iteraciones: {NUM_ITERACIONES}, Descarte (Burn-in): {BURN_IN}")
print("-" * 50)
print("Distribución de Probabilidad Aproximada:")
for valor, prob in resultado.items():
    print(f"  P({VARIABLE_CONSULTA}={valor} | Evidencia) ≈ {prob:.4f}")