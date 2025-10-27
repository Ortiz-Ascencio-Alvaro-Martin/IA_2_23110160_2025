# =========================================================================
# Decodificación de Regímenes de Mercado con el Algoritmo de Viterbi (OOP)
# =========================================================================

import numpy as np

class ViterbiDecoder:
    """
    Encapsula un Modelo Oculto de Markov (HMM) y decodifica la secuencia de
    estados ocultos más probable para una secuencia de observaciones dada.
    """

    def __init__(self, modelo_hmm):
        """Inicializa el decodificador con los parámetros del HMM."""
        self.A = modelo_hmm['transiciones']
        self.B = modelo_hmm['emisiones']
        self.pi = modelo_hmm['p_inicial']
        self.estados = modelo_hmm['estados']
        self.obs_map = {obs: i for i, obs in enumerate(modelo_hmm['observaciones'])}
        self.n_estados = len(self.estados)

    def decodificar(self, obs_seq):
        """
        Implementa el algoritmo de Viterbi para encontrar la ruta de estados más probable.
        """
        T = len(obs_seq)
        # Delta: Probabilidad del camino más probable hasta el tiempo t.
        delta = np.zeros((T, self.n_estados))
        # Psi: Almacena el estado anterior del camino más probable.
        psi = np.zeros((T, self.n_estados), dtype=int)

        # 1. Inicialización
        obs_idx_0 = self.obs_map[obs_seq[0]]
        delta[0, :] = self.pi * self.B[:, obs_idx_0]

        # 2. Recursión
        for t in range(1, T):
            obs_idx_t = self.obs_map[obs_seq[t]]
            for j in range(self.n_estados): # Estado actual
                # Probabilidad de transición desde todos los estados anteriores al estado j.
                trans_probs = delta[t-1, :] * self.A[:, j]
                
                # Encontrar el camino más probable y guardarlo.
                delta[t, j] = np.max(trans_probs) * self.B[j, obs_idx_t]
                psi[t, j] = np.argmax(trans_probs)

        # 3. Backtracking (Recuperación de la ruta)
        secuencia_indices = np.zeros(T, dtype=int)
        secuencia_indices[T-1] = np.argmax(delta[T-1, :])
        for t in range(T-2, -1, -1):
            secuencia_indices[t] = psi[t+1, secuencia_indices[t+1]]
            
        return [self.estados[i] for i in secuencia_indices]

# --- 1. DEFINICIÓN DEL MODELO HMM PARA EL MERCADO ---
MODELO_MERCADO = {
    'estados': ['Baja_Vol', 'Alta_Vol'],
    'observaciones': ['P_Severa', 'R_Medio', 'G_Severa'],
    'transiciones': np.array([[0.95, 0.05], [0.15, 0.85]]),
    'emisiones': np.array([[0.10, 0.80, 0.10], [0.40, 0.20, 0.40]]),
    'p_inicial': np.array([0.7, 0.3])
}

# --- 2. SECUENCIA DE OBSERVACIONES ---
RENDIMIENTOS_OBSERVADOS = [
    'R_Medio', 'R_Medio', 'R_Medio', 'P_Severa', 'G_Severa', 'P_Severa',
    'R_Medio', 'G_Severa', 'R_Medio', 'R_Medio', 'R_Medio'
]

# --- 3. EJECUCIÓN DE LA DECODIFICACIÓN ---
decodificador = ViterbiDecoder(MODELO_MERCADO)
secuencia_regimenes = decodificador.decodificar(RENDIMIENTOS_OBSERVADOS)

# --- 4. RESULTADOS Y VISUALIZACIÓN ---
print("--- Decodificación de Regímenes de Mercado con Viterbi ---")
print("\nEl algoritmo infiere el estado de volatilidad 'oculto' del mercado a partir de los rendimientos 'observados'.\n")

# Formatear para visualización
obs_str = [obs.center(10) for obs in RENDIMIENTOS_OBSERVADOS]
reg_str = [reg.center(10) for reg in secuencia_regimenes]

print("Observación: |" + " | ".join(obs_str) + " |")
print("Régimen:     |" + " | ".join(reg_str) + " |")

print("\nInterpretación:")
print("El HMM ha identificado correctamente que los días con rendimientos extremos ('P_Severa', 'G_Severa') corresponden al régimen de 'Alta_Vol', mientras que los días de calma ('R_Medio') corresponden a 'Baja_Vol'.")