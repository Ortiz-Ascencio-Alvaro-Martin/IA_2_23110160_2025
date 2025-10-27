# =========================================================================
# Inferencia Bayesiana Simple (Versión Orientada a Objetos)
# Problema: Determinar la probabilidad real de un defecto dado que
#           una alarma ha sonado.
# =========================================================================

class BayesianInferenceEngine:
    """
    Encapsula un modelo bayesiano simple para calcular la probabilidad a posteriori
    de una hipótesis (H) dada una evidencia (E).
    """

    def __init__(self, hipotesis, p_hipotesis, p_evidencia_dado_hipotesis):
        """
        Inicializa el motor con el conocimiento del modelo.
        - hipotesis: El nombre de la hipótesis principal (ej. 'Defectuoso').
        - p_hipotesis: La probabilidad a priori de esa hipótesis, P(H).
        - p_evidencia_dado_hipotesis: Un diccionario con P(E|H) y P(E|¬H).
        """
        self.hipotesis = hipotesis
        self.no_hipotesis = f"No {hipotesis}"
        
        # Probabilidades a priori
        self.p_h = p_hipotesis
        self.p_no_h = 1 - p_hipotesis
        
        # Verosimilitudes
        self.p_e_dado_h = p_evidencia_dado_hipotesis[True]
        self.p_e_dado_no_h = p_evidencia_dado_hipotesis[False]

    def inferir(self):
        """
        Aplica el Teorema de Bayes para calcular P(H | E).
        """
        # --- 1. Calcular el numerador: P(E | H) * P(H) ---
        numerador = self.p_e_dado_h * self.p_h
        
        # --- 2. Calcular el denominador P(E) usando la Ley de Probabilidad Total ---
        # P(E) = P(E | H) * P(H) + P(E | ¬H) * P(¬H)
        denominador = (self.p_e_dado_h * self.p_h) + (self.p_e_dado_no_h * self.p_no_h)
        
        # --- 3. Calcular la probabilidad a posteriori ---
        if denominador == 0:
            return 0
        
        p_h_dado_e = numerador / denominador
        return p_h_dado_e

# --- 1. DEFINICIÓN DEL MODELO ---
# Se agrupan los parámetros del problema.

# Hipótesis: La pieza es 'Defectuosa'.
# Evidencia: La 'Alarma' sonó.

# Probabilidad a priori de que una pieza sea defectuosa.
PROBABILIDAD_A_PRIORI = 0.01 # P(Defectuoso)

# Verosimilitudes: qué tan confiable es la alarma.
VEROSIMILITUDES = {
    True:  0.95, # P(Alarma | Defectuoso) - Tasa de Verdaderos Positivos
    False: 0.05  # P(Alarma | No Defectuoso) - Tasa de Falsos Positivos
}

# --- 2. EJECUCIÓN DE LA INFERENCIA ---
# Se crea una instancia del motor de inferencia con nuestro modelo.
motor_bayesiano = BayesianInferenceEngine(
    hipotesis='Defectuoso',
    p_hipotesis=PROBABILIDAD_A_PRIORI,
    p_evidencia_dado_hipotesis=VEROSIMILITUDES
)

# Se le pide que realice la inferencia.
probabilidad_final = motor_bayesiano.inferir()

# --- 3. RESULTADOS ---
print("--- Inferencia Bayesiana: ¿Es real la alarma del detector? ---")

print(f"\nCreencia Inicial (A Priori):")
print(f"  P({motor_bayesiano.hipotesis}) = {motor_bayesiano.p_h:.2%}")

print(f"\nCreencia Actualizada (A Posteriori):")
print(f"  P({motor_bayesiano.hipotesis} | Alarma) = {probabilidad_final:.2%}")
print(f"  P({motor_bayesiano.no_hipotesis} | Alarma) = {1 - probabilidad_final:.2%}")

print("\nConclusión: Aunque el detector es bastante preciso, la baja probabilidad inicial de un defecto significa que una alarma solo aumenta nuestra creencia a un 16.1%. Es más probable que sea una falsa alarma.")