# =========================================================================
# Filtro de Bayes para un Modelo Oculto de Markov (HMM)
# Implementación Orientada a Objetos
# Problema: Inferir el estado de un robot (Limpio/Sucio) a partir de
# observaciones ruidosas.
# =========================================================================

import numpy as np

class FiltroOcultoDeMarkov:
    """
    Encapsula un Modelo Oculto de Markov (HMM) y realiza inferencia de
    filtrado para estimar el estado actual basándose en una secuencia de
    observaciones.
    """

    def __init__(self, modelo):
        """
        Inicializa el filtro con los parámetros del modelo HMM.
        """
        self.estados = modelo['estados']
        self.observaciones = modelo['observaciones']
        self.s_map = {estado: i for i, estado in enumerate(self.estados)}
        self.o_map = {obs: i for i, obs in enumerate(self.observaciones)}
        
        # Parámetros del modelo
        self.prior = modelo['prob_inicial']
        self.transicion = modelo['prob_transicion']
        self.emision = modelo['prob_emision']
        
        # La creencia inicial es la probabilidad a priori de los estados.
        self.creencia_actual = self.prior.copy()

    def filtrar(self, secuencia_obs):
        """
        Procesa una secuencia completa de observaciones y actualiza la creencia
        en cada paso, aplicando el algoritmo de avance (Forward Algorithm).
        """
        historial = [self.creencia_actual]
        print(f"Creencia Inicial: P(Limpio)={self.creencia_actual[0]:.4f}, P(Sucio)={self.creencia_actual[1]:.4f}")

        for obs in secuencia_obs:
            obs_idx = self.o_map[obs]
            
            # --- 1. Paso de Predicción (Paso Temporal) ---
            # Se predice el estado futuro basándose en la creencia actual y el modelo de transición.
            # P(Z_t+1 | E_1:t) = Σ [ P(Z_t+1 | Z_t) * P(Z_t | E_1:t) ]
            # En notación matricial: b_predicha = T' * b_actual
            creencia_predicha = self.transicion.T @ self.creencia_actual
            
            # --- 2. Paso de Actualización (Paso de Observación) ---
            # Se corrige la predicción usando la nueva observación.
            # P(Z_t+1 | E_1:t+1) = α * P(E_t+1 | Z_t+1) * P(Z_t+1 | E_1:t)
            # En notación matricial: b_nueva = α * O_e * b_predicha
            creencia_no_normalizada = self.emision[:, obs_idx] * creencia_predicha
            
            # α es el factor de normalización para que las probabilidades sumen 1.
            alfa = np.sum(creencia_no_normalizada)
            self.creencia_actual = creencia_no_normalizada / alfa
            
            historial.append(self.creencia_actual)

        return historial

# --- 1. DEFINICIÓN DEL MODELO HMM ---
# Agrupar todos los parámetros en un único diccionario.
MODELO_ROBOT = {
    'estados': ['Limpio', 'Sucio'],
    'observaciones': ['OK', 'RUIDO'],
    'prob_inicial': np.array([0.8, 0.2]), # P(Z0)
    'prob_transicion': np.array([ # P(Z_t+1 | Z_t)
        [0.7, 0.3], # Limpio -> (Limpio, Sucio)
        [0.1, 0.9]  # Sucio  -> (Limpio, Sucio)
    ]),
    'prob_emision': np.array([ # P(E_t | Z_t)
        [0.9, 0.1], # Limpio -> (OK, RUIDO)
        [0.2, 0.8]  # Sucio  -> (OK, RUIDO)
    ])
}

# --- 2. SECUENCIA DE OBSERVACIONES ---
secuencia_de_evidencia = ['RUIDO', 'RUIDO', 'RUIDO', 'OK']

# --- 3. EJECUCIÓN DEL FILTRADO ---
print("--- Inferencia en un Modelo Oculto de Markov (Filtrado) ---")

# Se crea una instancia del filtro con nuestro modelo.
filtro = FiltroOcultoDeMarkov(MODELO_ROBOT)

# Se procesa la secuencia de evidencia.
historial_de_creencias = filtro.filtrar(secuencia_de_evidencia)

# --- 4. RESULTADOS ---
print("\n" + "=" * 60)
print("Historial de la Evolución de la Creencia:")
for t, creencia in enumerate(historial_de_creencias):
    print(f"  Paso {t} (Después de obs '{secuencia_de_evidencia[t-1]}' si t>0): ", end="")
    print(f"P(Limpio)={creencia[0]:.4f}, P(Sucio)={creencia[1]:.4f}")

print("\nCreencia Final después de toda la secuencia:")
creencia_final = historial_de_creencias[-1]
print(f"  P(Estado | {secuencia_de_evidencia}) = Limpio: {creencia_final[0]:.4f}, Sucio: {creencia_final[1]:.4f}")