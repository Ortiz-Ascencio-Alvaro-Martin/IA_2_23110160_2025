# =========================================================================
# Clasificador de Spam con Naive Bayes (Versión Orientada a Objetos)
# =========================================================================

class ClasificadorBayesiano:
    """
    Encapsula un modelo Naive Bayes simple para clasificación de texto.
    Conoce las probabilidades a priori y las verosimilitudes, y puede
    calcular la probabilidad a posteriori para clasificar nueva evidencia.
    """

    def __init__(self, probabilidades_a_priori, verosimilitudes):
        """
        Inicializa el clasificador con su conocimiento del mundo.
        - probabilidades_a_priori: Un diccionario P(Clase).
        - verosimilitudes: Un diccionario anidado P(Evidencia | Clase).
        """
        self.clases = list(probabilidades_a_priori.keys())
        self.a_priori = probabilidades_a_priori
        self.verosimilitudes = verosimilitudes

    def clasificar(self, evidencia):
        """
        Calcula la probabilidad a posteriori P(Clase | Evidencia) para cada
        clase y devuelve la clasificación más probable.
        """
        # --- 1. Calcular el denominador: P(Evidencia) ---
        # P(E) = Σ [ P(E | C) * P(C) ] para todas las clases C.
        prob_evidencia = sum(
            self.verosimilitudes[clase][evidencia] * self.a_priori[clase]
            for clase in self.clases
        )

        # --- 2. Calcular la probabilidad a posteriori para cada clase ---
        probabilidades_a_posteriori = {}
        for clase in self.clases:
            # Numerador: P(Evidencia | Clase) * P(Clase)
            numerador = self.verosimilitudes[clase][evidencia] * self.a_priori[clase]
            
            # Teorema de Bayes: P(Clase | Evidencia) = Numerador / Denominador
            a_posteriori = numerador / prob_evidencia
            probabilidades_a_posteriori[clase] = a_posteriori
        
        # --- 3. Determinar la clasificación final ---
        # Se elige la clase con la mayor probabilidad a posteriori.
        clasificacion_final = max(probabilidades_a_posteriori, key=probabilidades_a_posteriori.get)
        
        return clasificacion_final, probabilidades_a_posteriori

# --- 1. DEFINICIÓN DEL MODELO ---
# Probabilidades a priori (qué tan común es cada clase en general)
PRIORIS = {
    'Spam': 0.4,
    'NoSpam': 0.6
}

# Verosimilitudes (qué tan probable es ver la palabra 'Descuento' en cada tipo de correo)
VEROSIMILITUDES = {
    'Spam':   {'Descuento': 0.7},
    'NoSpam': {'Descuento': 0.1}
}

# La evidencia que queremos clasificar
EVIDENCIA_A_CLASIFICAR = 'Descuento'

# --- 2. EJECUCIÓN DEL CLASIFICADOR ---
# Se crea una instancia del clasificador con nuestro modelo.
clasificador = ClasificadorBayesiano(PRIORIS, VEROSIMILITUDES)

# Se le pide que clasifique la nueva evidencia.
resultado, probabilidades = clasificador.clasificar(EVIDENCIA_A_CLASIFICAR)

# --- 3. RESULTADOS ---
print(f"--- Clasificación de un correo con la palabra '{EVIDENCIA_A_CLASIFICAR}' ---")
print("\nProbabilidades a Posteriori calculadas:")
for clase, prob in probabilidades.items():
    print(f"  - P({clase} | '{EVIDENCIA_A_CLASIFICAR}'): {prob:.4f}")

print("\n--- Decisión Final ---")
print(f"Clasificación: ¡{resultado.upper()}!")