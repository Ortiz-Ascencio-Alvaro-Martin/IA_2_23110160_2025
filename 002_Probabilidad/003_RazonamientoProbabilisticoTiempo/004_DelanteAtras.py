# =========================================================================
# Algoritmo Forward-Backward para Suavizado en HMM (Versión OOP)
# =========================================================================

import numpy as np
import matplotlib.pyplot as plt

class HiddenMarkovModel:
    """
    Encapsula un Modelo Oculto de Markov y proporciona métodos para realizar
    inferencia, incluyendo el suavizado con el algoritmo Forward-Backward.
    """

    def __init__(self, transiciones, emisiones, p_inicial, estados, observaciones):
        self.A = transiciones
        self.B = emisiones
        self.pi = p_inicial
        self.estados = estados
        self.obs_map = {obs: i for i, obs in enumerate(observaciones)}
        self.n_estados = len(estados)

    def _forward_pass(self, obs_seq):
        """Calcula y devuelve la matriz alpha (mensajes de avance)."""
        T = len(obs_seq)
        alpha = np.zeros((T, self.n_estados))
        
        # Inicialización
        alpha[0, :] = self.pi * self.B[:, self.obs_map[obs_seq[0]]]
        
        # Recursión
        for t in range(1, T):
            alpha[t, :] = (alpha[t-1, :] @ self.A) * self.B[:, self.obs_map[obs_seq[t]]]
        
        # Se normaliza cada paso para evitar underflow numérico.
        alpha /= np.sum(alpha, axis=1, keepdims=True)
        return alpha

    def _backward_pass(self, obs_seq):
        """Calcula y devuelve la matriz beta (mensajes de retroceso)."""
        T = len(obs_seq)
        beta = np.zeros((T, self.n_estados))
        
        # Inicialización
        beta[T-1, :] = 1.0
        
        # Recursión (hacia atrás)
        for t in range(T - 2, -1, -1):
            # La operación se puede vectorizar para mayor eficiencia.
            beta[t, :] = self.A @ (self.B[:, self.obs_map[obs_seq[t+1]]] * beta[t+1, :])
            # Se normaliza para consistencia y estabilidad numérica.
            beta[t, :] /= np.sum(beta[t, :])
            
        return beta

    def smooth(self, obs_seq):
        """
        Calcula las probabilidades suavizadas para TODA la secuencia.
        P(X_k | E_1:T) para todo k.
        """
        alpha = self._forward_pass(obs_seq)
        beta = self._backward_pass(obs_seq)
        
        # 1. Combinar los mensajes: gamma = alpha * beta
        gamma = alpha * beta
        
        # 2. Normalizar en cada paso de tiempo para obtener la distribución final.
        prob_suavizada = gamma / np.sum(gamma, axis=1, keepdims=True)
        
        # También devuelve las probabilidades filtradas (alpha) para comparación.
        return prob_suavizada, alpha

# --- 1. DEFINICIÓN DEL MODELO HMM ---
ESTADOS_HMM = ['Normal', 'Fallo']
OBSERVACIONES_HMM = ['Bajo', 'Medio', 'Alto']

MODELO = {
    'transiciones': np.array([[0.9, 0.1], [0.3, 0.7]]),
    'emisiones': np.array([[0.8, 0.15, 0.05], [0.05, 0.25, 0.7]]),
    'p_inicial': np.array([0.5, 0.5]),
    'estados': ESTADOS_HMM,
    'observaciones': OBSERVACIONES_HMM
}

# --- 2. EJECUCIÓN DEL ALGORITMO ---
SECUENCIA_EVIDENCIA = ['Bajo', 'Bajo', 'Medio', 'Alto', 'Alto']
motor_hmm = HiddenMarkovModel(**MODELO)

# Se calculan las probabilidades suavizadas y filtradas para toda la secuencia.
prob_suavizadas, prob_filtradas = motor_hmm.smooth(SECUENCIA_EVIDENCIA)

# Tiempo de interés para el análisis (k=2, que es el Día 3).
K_TIME = 2

# --- 3. RESULTADOS Y VISUALIZACIÓN ---
print("--- Algoritmo Forward-Backward (Suavizado) ---")
print(f"Secuencia de Observaciones: {SECUENCIA_EVIDENCIA}")

print(f"\n--- Comparación de Creencias en el Día {K_TIME + 1} ---")
print("1. Probabilidad Filtrada (usando evidencia hasta el Día 3):")
for i, estado in enumerate(ESTADOS_HMM):
    print(f"   P({estado} | E_1:3) = {prob_filtradas[K_TIME, i]:.4f}")

print("\n2. Probabilidad Suavizada (usando TODA la evidencia hasta el Día 5):")
for i, estado in enumerate(ESTADOS_HMM):
    print(f"   P({estado} | E_1:5) = {prob_suavizadas[K_TIME, i]:.4f}")

# --- Gráfica Comparativa ---
plt.figure(figsize=(10, 5))
dias = np.arange(1, len(SECUENCIA_EVIDENCIA) + 1)
plt.plot(dias, prob_filtradas[:, 1], 'o--', label='Filtrado P(Fallo | E_1:t)', color='skyblue')
plt.plot(dias, prob_suavizadas[:, 1], 'o-', label='Suavizado P(Fallo | E_1:T)', color='darkblue', linewidth=2)
plt.title('Comparación de Probabilidad de Fallo: Filtrado vs. Suavizado')
plt.xlabel('Día (t)')
plt.ylabel('Probabilidad de Fallo')
plt.xticks(dias)
plt.legend()
plt.grid(True, alpha=0.5, linestyle=':')
plt.show()