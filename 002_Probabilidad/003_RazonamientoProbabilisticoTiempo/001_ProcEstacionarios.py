# =========================================================================
# Simulación de un Proceso NO Estacionario (Caminata Aleatoria con Deriva)
# =========================================================================

import numpy as np
import matplotlib.pyplot as plt

# --- Parámetros de la simulación ---
N = 500          # Número de puntos en la serie temporal
c = 0.05         # Media (intercepto), ahora actúa como una "deriva"
phi = 1.0        # Coeficiente AR(1). NO ESTACIONARIO porque |phi| >= 1
sigma_e = 1.0    # Desviación estándar del ruido

# --- 1. Generación del Ruido Blanco ---
# El ruido sigue siendo una secuencia de shocks aleatorios e independientes.
ruido = np.random.normal(loc=0, scale=sigma_e, size=N)

# --- 2. Generación del Proceso AR(1) NO Estacionario ---
# Con phi=1, esto se conoce como una "caminata aleatoria" (random walk).
# Con c != 0, es una "caminata aleatoria con deriva".
X = np.zeros(N)
X[0] = ruido[0]

# Generamos la serie temporal paso a paso
for t in range(1, N):
    # Xt = c + phi * X_{t-1} + epsilon_t
    # Como phi=1, cada nuevo valor es el valor anterior más un shock aleatorio y una deriva.
    X[t] = c + phi * X[t-1] + ruido[t]

# --- 3. Verificación de la No Estacionariedad ---
# En un proceso no estacionario, la media y la varianza cambian con el tiempo.
# Por lo tanto, calcular una media o varianza teórica constante no tiene sentido.

print("--- Proceso NO Estacionario (Caminata Aleatoria con Deriva) ---")
print(f"Parámetro phi: {phi} (>= 1, lo que causa la no estacionariedad)")
print("La media y la varianza de este proceso no son constantes en el tiempo.")
print("-" * 40)
# La media y varianza muestrales solo describen esta realización particular.
print(f"Media muestral (solo descriptiva): {np.mean(X):.3f}")
print(f"Varianza muestral (solo descriptiva): {np.var(X):.3f}")

# --- 4. Visualización ---
# El gráfico mostrará una clara tendencia, en lugar de fluctuar alrededor de una media.
plt.figure(figsize=(12, 5))
plt.plot(X, label=f'Serie No Estacionaria AR(1) con $\phi$={phi}', color='darkred')
plt.title('Ejemplo de un Proceso No Estacionario (Caminata Aleatoria)')
plt.xlabel('Tiempo')
plt.ylabel('Valores de $X_t$')
plt.legend()
plt.grid(True, alpha=0.5)
plt.show()