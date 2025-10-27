# =========================================================================
# Inferencia Aproximada con Ponderación de Verosimilitud (Versión OOP)
# =========================================================================

import random

class LikelihoodWeightingSampler:
    """
    Representa una Red Bayesiana y puede realizar inferencia aproximada
    utilizando el algoritmo de Ponderación de Verosimilitud.
    """

    def __init__(self, red_bayesiana):
        """
        Inicializa el muestreador con la estructura y las CPTs de la red.
        """
        self.nodos = red_bayesiana['nodos'] # Nodos en orden topológico
        self.padres = red_bayesiana['padres']
        self.cpts = red_bayesiana['cpts']
        print("Muestreador de Ponderación de Verosimilitud inicializado.")

    def _generar_muestra_ponderada(self, evidencia):
        """
        Genera una única muestra y su peso correspondiente.
        """
        muestra = {}
        peso = 1.0

        # Iterar sobre las variables en orden topológico.
        for variable in self.nodos:
            padres_de_var = self.padres[variable]
            # Obtener la configuración actual de los padres a partir de la muestra.
            configuracion_padres = tuple(muestra[p] for p in padres_de_var)

            if variable in evidencia:
                # 1. Si la variable es EVIDENCIA:
                #    - Se fija su valor.
                #    - Se multiplica el peso por P(evidencia | padres).
                valor_fijado = evidencia[variable]
                muestra[variable] = valor_fijado
                
                prob_evidencia = self.cpts[variable][configuracion_padres][valor_fijado]
                peso *= prob_evidencia
            else:
                # 2. Si la variable NO es evidencia:
                #    - Se muestrea su valor a partir de P(Variable | padres).
                prob_dist = self.cpts[variable][configuracion_padres]
                
                # Muestreo estocástico
                rand_val = random.random()
                cumulative_prob = 0.0
                for valor, prob in prob_dist.items():
                    cumulative_prob += prob
                    if rand_val < cumulative_prob:
                        muestra[variable] = valor
                        break
        
        return muestra, peso

    def inferir(self, var_consulta, evidencia, num_muestras):
        """
        Estima la distribución de probabilidad P(Consulta | Evidencia).
        """
        # Inicializar un diccionario para acumular los pesos para cada valor de la consulta.
        pesos_acumulados = {valor: 0.0 for valor in self.cpts[var_consulta]['valores']}

        for _ in range(num_muestras):
            # a) Generar una muestra ponderada.
            muestra, peso = self._generar_muestra_ponderada(evidencia)
            
            # b) Acumular el peso en la categoría correspondiente de la variable de consulta.
            valor_de_consulta_en_muestra = muestra[var_consulta]
            pesos_acumulados[valor_de_consulta_en_muestra] += peso
            
        # c) Normalizar los pesos acumulados para obtener la distribución de probabilidad final.
        total_pesos = sum(pesos_acumulados.values())
        if total_pesos == 0:
            return {valor: 0 for valor in pesos_acumulados}
            
        distribucion_final = {valor: peso / total_pesos for valor, peso in pesos_acumulados.items()}
        return distribucion_final

# --- 1. DEFINICIÓN DEL MODELO DE LA RED ---
# Se define la estructura y las CPTs de la red de forma general.
RED_ASPERSOR = {
    'nodos': ['Lluvia', 'Aspersor', 'Humedo'], # Orden topológico
    'padres': {
        'Lluvia': [],
        'Aspersor': [],
        'Humedo': ['Lluvia', 'Aspersor']
    },
    'cpts': {
        'Lluvia': {
            'valores': ['Si', 'No'],
            (): {'Si': 0.2, 'No': 0.8}
        },
        'Aspersor': {
            'valores': ['Si', 'No'],
            (): {'Si': 0.1, 'No': 0.9}
        },
        'Humedo': {
            'valores': ['Si', 'No'],
            ('Si', 'Si'): {'Si': 0.99, 'No': 0.01},
            ('Si', 'No'): {'Si': 0.90, 'No': 0.10},
            ('No', 'Si'): {'Si': 0.90, 'No': 0.10},
            ('No', 'No'): {'Si': 0.01, 'No': 0.99}
        }
    }
}

# --- 2. CONFIGURACIÓN DE LA INFERENCIA ---
VARIABLE_CONSULTA = 'Lluvia'
EVIDENCIA = {'Humedo': 'Si'}
NUM_MUESTRAS_TOTALES = 100000

# --- 3. EJECUCIÓN ---
muestreador_lw = LikelihoodWeightingSampler(RED_ASPERSOR)
resultado = muestreador_lw.inferir(VARIABLE_CONSULTA, EVIDENCIA, NUM_MUESTRAS_TOTALES)

# --- 4. RESULTADOS ---
print(f"--- Inferencia con Ponderación de Verosimilitud ---")
print(f"Consulta: P({VARIABLE_CONSULTA} | {list(EVIDENCIA.keys())[0]}='{list(EVIDENCIA.values())[0]}')")
print(f"Total de muestras generadas: {NUM_MUESTRAS_TOTALES}")
print("-" * 50)
print("Distribución de Probabilidad Aproximada:")
for valor, prob in resultado.items():
    print(f"  P({VARIABLE_CONSULTA}={valor} | Evidencia) ≈ {prob:.4f}")