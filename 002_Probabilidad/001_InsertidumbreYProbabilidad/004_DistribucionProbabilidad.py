# =========================================================================
# Estimación de una Distribución de Probabilidad con SciPy
# Objetivo: Modelar un conjunto de datos como una distribución normal.
# =========================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm # Importar el objeto de distribución normal

# --- 1. DATOS DE ENTRADA ---
# Muestra de temperaturas corporales observadas.
datos_temperatura = np.array([
    37.05, 36.88, 37.15, 36.92, 37.01, 37.20, 36.75, 37.08, 36.95, 37.10,
    37.02, 36.85, 37.18, 36.95, 37.00, 37.15, 36.80, 37.05, 36.90, 37.12,
    37.00, 36.99, 37.01, 37.00, 36.98, 37.03, 36.97, 37.04, 36.96, 37.02,
    37.00, 37.05, 37.00, 36.95, 37.05, 36.90, 37.10, 36.85, 37.15, 37.00
])

# --- 2. ESTIMACIÓN DE PARÁMETROS (MLE) ---
# Para una distribución normal, la Estimación de Máxima Verosimilitud (MLE)
# de la media y la desviación estándar son simplemente el promedio y la
# desviación estándar de la muestra.
media_estimada, std_estimada = norm.fit(datos_temperatura)

# --- 3. CREACIÓN Y VISUALIZACIÓN DEL MODELO ---
# Se genera un rango de valores de temperatura para graficar la curva.
x_valores = np.linspace(datos_temperatura.min() - 0.2, datos_temperatura.max() + 0.2, 200)

# Se calcula la PDF para el rango de valores usando el modelo ajustado.
pdf_estimada = norm.pdf(x_valores, loc=media_estimada, scale=std_estimada)

# --- 4. GRÁFICA DE RESULTADOS ---
plt.figure(figsize=(10, 6))

# a) Dibujar el histograma de los datos observados.
plt.hist(datos_temperatura, bins=10, density=True, alpha=0.7, color='skyblue', label='Datos Observados (Histograma)')

# b) Dibujar la curva de la distribución normal estimada. 
plt.plot(x_valores, pdf_estimada, 'r-', linewidth=2, label=f'Modelo Normal Ajustado\n(μ={media_estimada:.2f}, σ={std_estimada:.2f})')

# c) Añadir detalles a la gráfica.
plt.title('Ajuste de una Distribución Normal a Datos de Temperatura')
plt.xlabel('Temperatura Corporal (°C)')
plt.ylabel('Densidad de Probabilidad')
plt.axvline(media_estimada, color='gray', linestyle='--', linewidth=1.5, label=f'Media = {media_estimada:.2f}')
plt.legend()
plt.grid(axis='y', linestyle=':', alpha=0.7)
plt.show()

print("--- Parámetros del Modelo Estimado ---")
print(f"Media (μ) estimada: {media_estimada:.4f} °C")
print(f"Desviación Estándar (σ) estimada: {std_estimada:.4f} °C")