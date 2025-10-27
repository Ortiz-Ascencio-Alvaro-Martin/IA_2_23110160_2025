# =========================================================================
# Cálculo de Probabilidad Conjunta en una Red Bayesiana (Versión OOP)
# =========================================================================

class BayesianNetwork:
    """
    Representa una Red Bayesiana simple y puede calcular la probabilidad
    conjunta de un evento completo usando la Regla de la Cadena.
    """

    def __init__(self, cpts):
        """
        Inicializa la red con sus Tablas de Probabilidad Condicional (CPTs).
        """
        self.cpts = cpts

    def calculate_joint_probability(self, evento):
        """
        Calcula la probabilidad conjunta P(Robo, Alarma, JuanLlama) para un
        evento específico (una asignación completa de valores a las variables).
        
        La fórmula (Regla de la Cadena) es:
        P(R, A, J) = P(J | A) * P(A | R) * P(R)
        """
        # Extraer los valores del evento de interés.
        valor_robo = evento['Robo']
        valor_alarma = evento['Alarma']
        valor_juanllama = evento['JuanLlama']
        
        # 1. Obtener P(Robo)
        p_robo = self.cpts['Robo'][valor_robo]
        
        # 2. Obtener P(Alarma | Robo)
        p_alarma_dado_robo = self.cpts['Alarma'][valor_robo][valor_alarma]
        
        # 3. Obtener P(JuanLlama | Alarma)
        p_juanllama_dado_alarma = self.cpts['JuanLlama'][valor_alarma][valor_juanllama]
        
        # 4. Multiplicar en cadena para obtener la probabilidad conjunta.
        joint_probability = p_juanllama_dado_alarma * p_alarma_dado_robo * p_robo
        
        return joint_probability

# --- 1. DEFINICIÓN DEL MODELO (CPTs) ---
# Se definen las tablas de probabilidad condicional de la red.
CPT_DEFINITIONS = {
    'Robo': {'Si': 0.001, 'No': 0.999},
    'Alarma': { # P(Alarma | Robo)
        'Si': {'Si': 0.95, 'No': 0.05},  # Dado Robo=Si
        'No': {'Si': 0.01, 'No': 0.99}   # Dado Robo=No
    },
    'JuanLlama': { # P(JuanLlama | Alarma)
        'Si': {'Si': 0.90, 'No': 0.10},  # Dado Alarma=Si
        'No': {'Si': 0.05, 'No': 0.95}   # Dado Alarma=No
    }
}

# --- 2. EJECUCIÓN DEL CÁLCULO ---
# Se crea una instancia de la red con el modelo definido.
red_alarma = BayesianNetwork(CPT_DEFINITIONS)

# Se define el evento específico para el cual queremos calcular la probabilidad.
evento_a_calcular = {
    'Robo': 'Si',
    'Alarma': 'No',
    'JuanLlama': 'Si'
}

# Se calcula la probabilidad conjunta.
probabilidad_final = red_alarma.calculate_joint_probability(evento_a_calcular)

# --- 3. RESULTADOS ---
print("--- Cálculo de Probabilidad Conjunta con la Regla de la Cadena ---")
print(f"Evento a calcular: P(Robo={evento_a_calcular['Robo']}, Alarma={evento_a_calcular['Alarma']}, JuanLlama={evento_a_calcular['JuanLlama']})")
print("-" * 70)
print(f"Resultado de la Probabilidad Conjunta: {probabilidad_final:.7f}")