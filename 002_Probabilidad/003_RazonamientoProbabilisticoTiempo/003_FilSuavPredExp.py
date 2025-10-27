# =========================================================================
# Motor de Inferencia para Modelos Ocultos de Markov (Versión OOP)
# Problema: Monitoreo del estado de salud de un paciente (Sano/Fiebre)
# =========================================================================

import numpy as np

class HiddenMarkovModel:
    """
    Encapsula un Modelo Oculto de Markov y proporciona métodos para realizar
    las tareas de inferencia clave: filtrado, predicción, suavizado y decodificación.
    """

    def __init__(self, transiciones, emisiones, p_inicial, estados, observaciones):
        self.A = transiciones
        self.B = emisiones
        self.pi = p_inicial
        self.estados = estados
        self.observaciones = observaciones
        self.n_estados = len(estados)
        self.obs_map = {obs: i for i, obs in enumerate(self.observaciones)}

    def _forward(self, obs_seq):
        """Calcula la matriz alpha (mensajes de avance)."""
        T = len(obs_seq)
        alpha = np.zeros((T, self.n_estados))
        
        # Inicialización
        alpha[0, :] = self.pi * self.B[:, self.obs_map[obs_seq[0]]]
        
        # Recursión
        for t in range(1, T):
            alpha[t, :] = (alpha[t-1, :] @ self.A) * self.B[:, self.obs_map[obs_seq[t]]]
        
        return alpha

    def _backward(self, obs_seq):
        """Calcula la matriz beta (mensajes de retroceso)."""
        T = len(obs_seq)
        beta = np.zeros((T, self.n_estados))
        
        # Inicialización (beta_T-1 = 1)
        beta[T-1, :] = 1.0
        
        # Recursión (desde T-2 hasta 0)
        for t in range(T-2, -1, -1):
            beta[t, :] = (self.A @ (self.B[:, self.obs_map[obs_seq[t+1]]] * beta[t+1, :]))
            
        return beta

    def filtrar(self, obs_seq):
        """1. Filtrado: P(X_t | E_1:t) - Creencia sobre el estado actual."""
        alpha = self._forward(obs_seq)
        # Normalizar el último mensaje de avance para obtener la distribución.
        return alpha[-1, :] / np.sum(alpha[-1, :])

    def predecir(self, obs_seq, k_pasos):
        """2. Predicción: P(X_{t+k} | E_1:t) - Creencia sobre un estado futuro."""
        # Primero, obtener la creencia sobre el estado actual.
        creencia_actual = self.filtrar(obs_seq)
        # Propagar la creencia k pasos hacia el futuro usando solo la matriz de transición.
        for _ in range(k_pasos):
            creencia_actual = creencia_actual @ self.A
        return creencia_actual

    def suavizar(self, obs_seq):
        """3. Suavizado: P(X_k | E_1:t) para k < t - Creencia revisada sobre un estado pasado."""
        alpha = self._forward(obs_seq)
        beta = self._backward(obs_seq)
        
        # P(X_k | E_1:t) = α * alpha_k * beta_k
        prob_suavizada = alpha * beta
        # Normalizar cada fila (cada paso de tiempo) para obtener la distribución.
        return prob_suavizada / np.sum(prob_suavizada, axis=1, keepdims=True)

    def decodificar_viterbi(self, obs_seq):
        """4. Decodificación: argmax P(X_1:t | E_1:t) - La secuencia de estados más probable."""
        T = len(obs_seq)
        delta = np.zeros((T, self.n_estados))
        psi = np.zeros((T, self.n_estados), dtype=int)

        # Inicialización
        delta[0, :] = self.pi * self.B[:, self.obs_map[obs_seq[0]]]
        
        # Recursión
        for t in range(1, T):
            for j in range(self.n_estados):
                trans_probs = delta[t-1, :] * self.A[:, j]
                delta[t, j] = np.max(trans_probs) * self.B[j, self.obs_map[obs_seq[t]]]
                psi[t, j] = np.argmax(trans_probs)

        # Backtracking
        secuencia_indices = np.zeros(T, dtype=int)
        secuencia_indices[T-1] = np.argmax(delta[T-1, :])
        for t in range(T-2, -1, -1):
            secuencia_indices[t] = psi[t+1, secuencia_indices[t+1]]
            
        return [self.estados[i] for i in secuencia_indices]

# --- 1. DEFINICIÓN DEL MODELO HMM ---
ESTADOS_HMM = ['Sano', 'Fiebre']
OBSERVACIONES_HMM = ['Normal', 'Frío', 'Caliente']

HMM_PACIENTE = {
    'transiciones': np.array([[0.7, 0.3], [0.4, 0.6]]),    # A: P(Xt | Xt-1)
    'emisiones': np.array([[0.5, 0.4, 0.1], [0.1, 0.3, 0.6]]), # B: P(Et | Xt)
    'p_inicial': np.array([0.6, 0.4]),                       # Pi: P(X0)
    'estados': ESTADOS_HMM,
    'observaciones': OBSERVACIONES_HMM
}

# --- 2. SECUENCIA DE OBSERVACIONES ---
# Observaciones de la temperatura del paciente durante 4 días.
SECUENCIA_OBS = ['Normal', 'Frío', 'Normal', 'Caliente']

# --- 3. EJECUCIÓN DE LA INFERENCIA ---
# Se crea una instancia del motor de inferencia con el modelo del paciente.
motor_hmm = HiddenMarkovModel(**HMM_PACIENTE)

# 1. Filtrado: ¿Cuál es la probabilidad de que el paciente tenga fiebre HOY (día 4)?
prob_filtrada = motor_hmm.filtrar(SECUENCIA_OBS)

# 2. Predicción: ¿Cuál será la probabilidad de que tenga fiebre MAÑANA?
prob_predicha = motor_hmm.predecir(SECUENCIA_OBS, k_pasos=1)

# 3. Suavizado: Con la información de hoy, ¿cuál era la probabilidad de que tuviera fiebre ANTEAYER (día 2)?
prob_suavizadas = motor_hmm.suavizar(SECUENCIA_OBS)

# 4. Decodificación: ¿Cuál fue la secuencia más probable de estados de salud durante los 4 días?
secuencia_mas_probable = motor_hmm.decodificar_viterbi(SECUENCIA_OBS)

# --- 4. RESULTADOS ---
print("--- Inferencia en un Modelo Oculto de Markov (Paciente) ---")
print(f"Secuencia de Observaciones: {SECUENCIA_OBS}\n")

print("1. FILTRADO: P(Salud_Día4 | Obs_1:4)")
for i, estado in enumerate(ESTADOS_HMM): print(f"  - {estado}: {prob_filtrada[i]:.4f}")

print("\n2. PREDICCIÓN: P(Salud_Día5 | Obs_1:4)")
for i, estado in enumerate(ESTADOS_HMM): print(f"  - {estado}: {prob_predicha[i]:.4f}")

print("\n3. SUAVIZADO: P(Salud_Día2 | Obs_1:4)")
for i, estado in enumerate(ESTADOS_HMM): print(f"  - {estado}: {prob_suavizadas[1][i]:.4f}")

print("\n4. DECODIFICACIÓN (Viterbi): Secuencia de salud más probable")
print(f"  -> {' -> '.join(secuencia_mas_probable)}")