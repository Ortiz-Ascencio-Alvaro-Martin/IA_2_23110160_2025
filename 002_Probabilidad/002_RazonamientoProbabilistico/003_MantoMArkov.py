# =========================================================================
# Inferencia con Manto de Markov en una Red Bayesiana (Versión OOP)
# Principio: Un nodo es condicionalmente independiente de todo el resto de la
# red, dado el estado de sus padres, sus hijos y los otros padres de sus hijos.
# =========================================================================

class RedBayesiana:
    """
    Representa una Red Bayesiana simple y puede realizar inferencia
    utilizando el principio del Manto de Markov.
    """

    def __init__(self, cpts, padres, hijos):
        """
        Inicializa la red con su estructura y tablas de probabilidad.
        """
        self.cpts = cpts
        self.padres = padres
        self.hijos = hijos

    def inferir_dado_manto_markov(self, nodo_consulta, evidencia):
        """
        Calcula P(Nodo | Manto de Markov)
        Para un nodo X, la fórmula se simplifica a:
        P(X | Manto) = α * P(X | Padres(X)) * Π P(Hijo_i | Padres(Hijo_i))
        """
        # 1. Verificar que la evidencia corresponde al Manto de Markov del nodo.
        manto_esperado = set(self.padres.get(nodo_consulta, []) + self.hijos.get(nodo_consulta, []))
        if set(evidencia.keys()) != manto_esperado:
            return f"Error: La evidencia proporcionada no es el Manto de Markov de '{nodo_consulta}'."

        distribucion_no_normalizada = {}

        # 2. Iterar sobre cada posible valor del nodo de consulta (ej. 'Si', 'No').
        for valor_consulta in self.cpts[nodo_consulta]['valores']:
            
            # --- Iniciar el cálculo del producto ---
            prob_producto = 1.0
            
            # a) Multiplicar por P(Nodo | Padres(Nodo))
            configuracion_padres = tuple(evidencia[p] for p in self.padres.get(nodo_consulta, []))
            prob_producto *= self.cpts[nodo_consulta][configuracion_padres][valor_consulta]

            # b) Multiplicar por cada P(Hijo | Padres(Hijo))
            for hijo in self.hijos.get(nodo_consulta, []):
                # La evidencia de los padres del hijo incluye al nodo de consulta y a la evidencia externa.
                evidencia_padres_hijo = evidencia.copy()
                evidencia_padres_hijo[nodo_consulta] = valor_consulta
                config_padres_hijo = tuple(evidencia_padres_hijo[p] for p in self.padres.get(hijo, []))
                
                # Obtener el valor del hijo desde la evidencia para buscar en la CPT.
                valor_hijo = evidencia[hijo]
                prob_producto *= self.cpts[hijo][config_padres_hijo][valor_hijo]
            
            distribucion_no_normalizada[valor_consulta] = prob_producto
            
        # 3. Normalizar para obtener la distribución de probabilidad final.
        normalizador = sum(distribucion_no_normalizada.values())
        if normalizador == 0: return {v: 0 for v in distribucion_no_normalizada}

        distribucion_final = {val: prob / normalizador for val, prob in distribucion_no_normalizada.items()}
        return distribucion_final

# --- 1. DEFINICIÓN DE LA ESTRUCTURA DE LA RED ---
ESTRUCTURA_RED = {
    'padres': {
        'Robo': [],
        'Alarma': ['Robo'],
        'JuanLlama': ['Alarma']
    },
    'hijos': { # Hijos de cada nodo (calculado para facilitar el acceso)
        'Robo': ['Alarma'],
        'Alarma': ['JuanLlama'],
        'JuanLlama': []
    },
    'cpts': {
        'Robo': {'valores': ['Si', 'No'], 'Si': 0.001, 'No': 0.999},
        'Alarma': {
            'valores': ['Si', 'No'],
            ('Si',): {'Si': 0.95, 'No': 0.05}, # P(Alarma | Robo=Si)
            ('No',): {'Si': 0.01, 'No': 0.99}  # P(Alarma | Robo=No)
        },
        'JuanLlama': {
            'valores': ['Si', 'No'],
            ('Si',): {'Si': 0.90, 'No': 0.10}, # P(JuanLlama | Alarma=Si)
            ('No',): {'Si': 0.05, 'No': 0.95}  # P(JuanLlama | Alarma=No)
        }
    }
}

# --- 2. EJECUCIÓN DE LA INFERENCIA ---
# Se crea una instancia del motor de inferencia con la estructura de la red.
motor_bn = RedBayesiana(ESTRUCTURA_RED['cpts'], ESTRUCTURA_RED['padres'], ESTRUCTURA_RED['hijos'])

# Se define la consulta y la evidencia (que es el Manto de Markov de 'Alarma').
NODO_CONSULTA = 'Alarma'
EVIDENCIA_MANTO = {
    'Robo': 'Si',       # Padre de 'Alarma'
    'JuanLlama': 'No'   # Hijo de 'Alarma'
}

# Se realiza la inferencia.
resultado = motor_bn.inferir_dado_manto_markov(NODO_CONSULTA, EVIDENCIA_MANTO)

# --- 3. RESULTADOS ---
print("--- Inferencia usando el Manto de Markov de 'Alarma' ---")
print(f"Consulta: P({NODO_CONSULTA} | {EVIDENCIA_MANTO})")
print("-" * 60)
print("Resultado de la Inferencia:")
for valor, probabilidad in resultado.items():
    print(f"  P({NODO_CONSULTA}={valor} | Evidencia) = {probabilidad:.4f}")