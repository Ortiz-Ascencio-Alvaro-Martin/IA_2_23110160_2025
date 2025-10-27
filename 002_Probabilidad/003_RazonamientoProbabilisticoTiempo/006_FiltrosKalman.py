# =========================================================================
# Filtro de Kalman para Seguimiento de Objetos (Versión Orientada a Objetos)
# =========================================================================

import numpy as np
import matplotlib.pyplot as plt

class KalmanFilter:
    """
    Implementa un Filtro de Kalman lineal para el seguimiento de estado.
    """
    def __init__(self, F, H, Q, R, x0, P0):
        """
        Inicializa el filtro con las matrices del modelo y el estado inicial.
        """
        self.F = F  # Matriz de transición de estado
        self.H = H  # Matriz de observación
        self.Q = Q  # Covarianza del ruido de proceso
        self.R = R  # Covarianza del ruido de medición
        
        self.x_hat = x0 # Estado estimado
        self.P = P0     # Covarianza del estado estimado

    def predict(self):
        """
        Fase de predicción: Proyecta el estado y la covarianza hacia adelante.
        """
        # x̂_k|k-1 = F * x̂_{k-1|k-1}
        self.x_hat = self.F @ self.x_hat
        # P_k|k-1 = F * P_{k-1|k-1} * F' + Q
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, z):
        """
        Fase de actualización: Corrige la predicción usando la nueva medición 'z'.
        """
        # --- Cálculo de la Ganancia de Kalman (K) ---
        # K = P_k|k-1 * H' * inv(H * P_k|k-1 * H' + R)
        S = self.H @ self.P @ self.H.T + self.R # Covarianza de la innovación
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # --- Actualización del estado con la medición ---
        # x̂_k|k = x̂_k|k-1 + K * (z_k - H * x̂_k|k-1)
        innovacion = z - self.H @ self.x_hat
        self.x_hat = self.x_hat + K @ innovacion
        
        # --- Actualización de la covarianza ---
        # P_k|k = (I - K * H) * P_k|k-1
        I = np.eye(self.P.shape[0])
        self.P = (I - K @ self.H) @ self.P

# --- 1. CONFIGURACIÓN DEL PROBLEMA Y DEL FILTRO ---
dt = 0.1
VELOCIDAD_REAL = 1.0
NUM_PASOS = 50

# Definición de las matrices del modelo
F_matrix = np.array([[1, dt], [0, 1]])
H_matrix = np.array([[1, 0]])
Q_matrix = np.array([[0.01, 0], [0, 0.01]])
R_matrix = np.array([[1.0]])

# Estado y covarianza iniciales
x0_initial = np.array([[0], [0]])
P0_initial = np.array([[100, 0], [0, 100]])

# Se crea una instancia del filtro
kf = KalmanFilter(F=F_matrix, H=H_matrix, Q=Q_matrix, R=R_matrix, x0=x0_initial, P0=P0_initial)

# --- 2. SIMULACIÓN DE DATOS ---
posicion_real = np.arange(NUM_PASOS) * dt * VELOCIDAD_REAL
np.random.seed(42)
mediciones = posicion_real + np.random.normal(0, np.sqrt(R_matrix[0, 0]), size=NUM_PASOS)

# --- 3. BUCLE PRINCIPAL DE FILTRADO ---
historial_estimaciones = []
for z_k in mediciones:
    # a) Fase de predicción
    kf.predict()
    # b) Fase de actualización
    kf.update(np.array([[z_k]]))
    # Guardar el resultado de la posición
    historial_estimaciones.append(kf.x_hat[0, 0])

# --- 4. VISUALIZACIÓN ---
plt.figure(figsize=(12, 6))
plt.plot(posicion_real, label='Posición Real (Verdad Oculta)', color='green', linewidth=2)
plt.scatter(range(NUM_PASOS), mediciones, label='Mediciones Ruidosas', color='red', alpha=0.5, marker='.')
plt.plot(historial_estimaciones, label='Estimación del Filtro de Kalman', color='blue', linewidth=2, linestyle='--')
plt.title('Seguimiento 1D con Filtro de Kalman')
plt.xlabel('Paso de Tiempo')
plt.ylabel('Posición (metros)')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.show()

print("--- Resultado del Filtro de Kalman ---")
print("La gráfica muestra cómo la estimación del filtro (línea azul discontinua) suaviza las mediciones ruidosas (puntos rojos) y sigue de cerca la trayectoria real (línea verde).")