# =========================================================================
# Inferencia en una Red Bayesiana Simple con Independencia Condicional
# Problema: Diagnóstico de Gripe a partir de Síntomas (Fiebre, Tos)
# =========================================================================

class RedBayesianaSimple:
    """
    Representa una red bayesiana simple donde los síntomas (Fiebre, Tos)
    son condicionalmente independientes dada la causa (Gripe).
    """

    def __init__(self, p_causa, p_efecto_dado_causa):
        """
        Inicializa la red con su estructura de probabilidades.
        - p_causa: Probabilidad a priori de la causa (ej. P(Gripe)).
        - p_efecto_dado_causa: Probabilidades condicionales de los efectos.
        """
        self.causa = list(p_causa.keys())[0]
        self.efectos = list(p_efecto_dado_causa.keys())
        self.p_causa = p_causa
        self.p_efecto = p_efecto_dado_causa

    def calcular_prob_conjunta(self, tiene_causa, tiene_efecto1, tiene_efecto2):
        """
        Calcula la probabilidad conjunta P(Causa, Efecto1, Efecto2) usando
        la regla de la cadena y la asunción de independencia condicional.
        P(C, E1, E2) = P(E1 | C) * P(E2 | C) * P(C)
        """
        # Determinar las probabilidades a usar basadas en si la causa está presente.
        if tiene_causa:
            p_c = self.p_causa[self.causa]
            p_e1_dado_c = self.p_efecto[self.efectos[0]][True] # P(E1 | C=True)
            p_e2_dado_c = self.p_efecto[self.efectos[1]][True] # P(E2 | C=True)
        else:
            p_c = 1 - self.p_causa[self.causa]
            p_e1_dado_c = self.p_efecto[self.efectos[0]][False] # P(E1 | C=False)
            p_e2_dado_c = self.p_efecto[self.efectos[1]][False] # P(E2 | C=False)
            
        return p_e1_dado_c * p_e2_dado_c * p_c

    def inferir_probabilidad(self, efecto_evidencia, efecto_pregunta):
        """
        Realiza una inferencia para calcular P(Pregunta | Evidencia).
        Ej. P(Fiebre | Tos) = P(Fiebre, Tos) / P(Tos)
        """
        # 1. Calcular P(Pregunta, Evidencia) usando la ley de probabilidad total.
        # P(F, T) = P(F, T, G) + P(F, T, ¬G)
        p_conjunta_con_causa = self.calcular_prob_conjunta(True, True, True)
        p_conjunta_sin_causa = self.calcular_prob_conjunta(False, True, True)
        p_ambos_efectos = p_conjunta_con_causa + p_conjunta_sin_causa

        # 2. Calcular P(Evidencia)
        # P(T) = P(T | G)*P(G) + P(T | ¬G)*P(¬G)
        p_evidencia = (self.p_efecto[efecto_evidencia][True] * self.p_causa[self.causa] +
                       self.p_efecto[efecto_evidencia][False] * (1 - self.p_causa[self.causa]))
        
        # 3. Calcular la probabilidad condicional final.
        if p_evidencia == 0:
            return 0
        return p_ambos_efectos / p_evidencia

# --- 1. DEFINICIÓN DEL MODELO ---
# Se agrupan todas las probabilidades en estructuras de datos claras.
PROBABILIDAD_A_PRIORI = {'Gripe': 0.05}

# P(Efecto | Causa)
PROBABILIDADES_CONDICIONALES = {
    'Fiebre': {True: 0.90, False: 0.10}, # P(Fiebre | Gripe=True/False)
    'Tos':    {True: 0.80, False: 0.05}  # P(Tos | Gripe=True/False)
}

# --- 2. EJECUCIÓN DEL ANÁLISIS ---
# Se crea una instancia de la red con nuestro modelo médico.
red_diagnostico = RedBayesianaSimple(PROBABILIDAD_A_PRIORI, PROBABILIDADES_CONDICIONALES)

# a) Calcular las probabilidades conjuntas clave.
p_f_t_g = red_diagnostico.calcular_prob_conjunta(tiene_causa=True, tiene_efecto1=True, tiene_efecto2=True)
p_f_t_nog = red_diagnostico.calcular_prob_conjunta(tiene_causa=False, tiene_efecto1=True, tiene_efecto2=True)

# b) Realizar una inferencia.
p_fiebre_dado_tos = red_diagnostico.inferir_probabilidad(efecto_evidencia='Tos', efecto_pregunta='Fiebre')

# --- 3. RESULTADOS ---
print("--- Inferencia en Red Bayesiana Simple ---")
print("Asunción: Fiebre y Tos son condicionalmente independientes dada la Gripe.")
print("-" * 60)
print("Cálculo de Probabilidades Conjuntas:")
print(f"  P(Fiebre, Tos, Gripe) = {p_f_t_g:.4f}")
print(f"  P(Fiebre, Tos, NO Gripe) = {p_f_t_nog:.4f}")
print("-" * 60)
print("Inferencia Final:")
print(f"  Probabilidad de P(Fiebre | Tos) = {p_fiebre_dado_tos:.4f}")
print("\nConclusión: Saber que un paciente tiene tos aumenta significativamente la probabilidad de que también tenga fiebre.")