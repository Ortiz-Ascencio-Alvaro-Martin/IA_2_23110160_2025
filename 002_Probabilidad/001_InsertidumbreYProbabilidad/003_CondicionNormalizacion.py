# =========================================================================
# Actualización de Creencias con el Teorema de Bayes (Versión Orientada a Objetos)
# Problema: Diagnóstico médico a partir de una prueba.
# =========================================================================

class BayesianUpdater:
    """
    Encapsula un modelo bayesiano simple y realiza inferencia.
    Calcula la probabilidad a posteriori de una hipótesis dada una evidencia.
    """

    def __init__(self, hipotesis, a_priori, verosimilitudes):
        """
        Inicializa el motor de inferencia con el conocimiento del modelo.
        - hipotesis: Una lista de posibles estados del mundo (ej. ['Enfermo', 'Sano']).
        - a_priori: Un diccionario con la probabilidad P(Hipótesis) para cada una.
        - verosimilitudes: Un diccionario anidado P(Evidencia | Hipótesis).
        """
        self.hipotesis = hipotesis
        self.a_priori = a_priori
        self.verosimilitudes = verosimilitudes

    def actualizar_creencia(self, evidencia):
        """
        Calcula la probabilidad a posteriori P(Hipótesis | Evidencia) para todas
        las hipótesis, dado que se ha observado una pieza de evidencia.
        """
        # --- 1. Calcular el denominador (Normalizador P(Evidencia)) ---
        # Se calcula usando la Ley de Probabilidad Total:
        # P(E) = Σ [ P(E | H) * P(H) ] para todas las hipótesis H.
        normalizador = sum(
            self.verosimilitudes[h][evidencia] * self.a_priori[h]
            for h in self.hipotesis
        )

        # --- 2. Calcular la probabilidad a posteriori para cada hipótesis ---
        a_posteriori = {}
        for h in self.hipotesis:
            # Numerador = P(Evidencia | Hipótesis) * P(Hipótesis)
            numerador = self.verosimilitudes[h][evidencia] * self.a_priori[h]
            
            # Teorema de Bayes: P(H | E) = Numerador / Normalizador
            a_posteriori[h] = numerador / normalizador
            
        return a_posteriori

# --- 1. DEFINICIÓN DEL MODELO ---
# Se agrupan todas las probabilidades en estructuras de datos claras.
HIPOTESIS_MEDICAS = ['Enfermo', 'Sano']

# Probabilidades a priori (creencia inicial antes de la prueba)
PRIORIS_MEDICOS = {
    'Enfermo': 0.01, # P(Enfermo)
    'Sano':    0.99  # P(Sano)
}

# Verosimilitudes (qué tan confiable es la prueba)
VEROSIMILITUDES_MEDICAS = {
    # P(Resultado de la Prueba | Estado Real)
    'Enfermo': {'Positivo': 0.99, 'Negativo': 0.01}, # Sensibilidad
    'Sano':    {'Positivo': 0.10, 'Negativo': 0.90}  # Tasa de Falsos Positivos
}

# La evidencia que se observó en el mundo real.
EVIDENCIA_OBSERVADA = 'Positivo'

# --- 2. EJECUCIÓN DE LA INFERENCIA ---
# Se crea una instancia del motor de inferencia con nuestro modelo médico.
inferencia = BayesianUpdater(HIPOTESIS_MEDICAS, PRIORIS_MEDICOS, VEROSIMILITUDES_MEDICAS)

# Se le pide que actualice la creencia basándose en la evidencia.
creencia_actualizada = inferencia.actualizar_creencia(EVIDENCIA_OBSERVADA)

# --- 3. RESULTADOS ---
print(f"--- Inferencia Bayesiana para un resultado de prueba '{EVIDENCIA_OBSERVADA}' ---")
print(f"\nCreencia Inicial (A Priori):")
print(f"  P(Enfermo) = {PRIORIS_MEDICOS['Enfermo']:.2%}")
print(f"  P(Sano)    = {PRIORIS_MEDICOS['Sano']:.2%}")

print(f"\nCreencia Actualizada (A Posteriori):")
for hipotesis, probabilidad in creencia_actualizada.items():
    print(f"  P({hipotesis} | {EVIDENCIA_OBSERVADA}) = {probabilidad:.2%}")

print("\nConclusión: A pesar de que la prueba es bastante precisa, la baja probabilidad inicial de la enfermedad hace que un resultado positivo solo aumente la creencia de estar enfermo a un 9%.")