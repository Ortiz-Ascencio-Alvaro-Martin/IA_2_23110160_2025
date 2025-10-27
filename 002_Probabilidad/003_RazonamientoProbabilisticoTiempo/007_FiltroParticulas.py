# =========================================================================
# Filtro de Partículas para Seguimiento no Lineal (Versión Orientada a Objetos)
# =========================================================================

import numpy as np
import matplotlib.pyplot as plt

class ParticleFilter:
    """
    Encapsula la lógica de un Filtro de Partículas (PF) para el seguimiento de estado.
    """

    def __init__(self, num_particulas, varianza_proceso, ancho_ruido_medicion):
        self.N = num_particulas
        self.var_proc = varianza_proceso
        self.ancho_ruido_med = ancho_ruido_medicion
        
        # Inicializar las partículas y sus pesos.
        self.particulas = np.random.uniform(-5, 5, self.N)
        self.pesos = np.ones(self.N) / self.N

    def predecir(self, velocidad, dt):
        """
        Fase de Predicción: Propaga las partículas hacia adelante en el tiempo
        usando el modelo de movimiento.
        """
        ruido_proceso = np.random.normal(0, np.sqrt(self.var_proc), self.N)
        self.particulas += velocidad * dt + ruido_proceso

    def actualizar(self, medicion):
        """
        Fase de Actualización: Re-pondera las partículas basándose en qué tan bien
        explican la nueva medición.
        """
        # Calcular la verosimilitud P(Medición | Partícula)
        diferencia = np.abs(medicion - self.particulas)
        verosimilitud = np.where(
            diferencia <= self.ancho_ruido_med,
            1.0 / (2.0 * self.ancho_ruido_med),
            1e-9 # Un valor muy pequeño en lugar de cero para estabilidad numérica
        )
        
        # Actualizar los pesos: w_nuevo = w_viejo * verosimilitud
        self.pesos *= verosimilitud
        
        # Normalizar los pesos para que sumen 1.
        self.pesos /= np.sum(self.pesos)

    def remuestrear(self):
        """
        Fase de Remuestreo: Elimina partículas con bajo peso y duplica las de alto peso
        para evitar la degeneración de las partículas.
        """
        indices = np.random.choice(self.N, size=self.N, p=self.pesos)
        self.particulas = self.particulas[indices]
        # Después del remuestreo, todos los pesos se resetean a ser iguales.
        self.pesos = np.ones(self.N) / self.N
        
    def estimar(self):
        """Calcula la estimación del estado actual como la media ponderada de las partículas."""
        return np.sum(self.particulas * self.pesos)

# --- 1. CONFIGURACIÓN DE LA SIMULACIÓN ---
T_PASOS = 50
DT = 1.0
VELOCIDAD_REAL = 0.5

# --- 2. SIMULACIÓN DE DATOS REALES ---
posicion_real = np.arange(T_PASOS) * DT * VELOCIDAD_REAL
mediciones = posicion_real + np.random.uniform(-2.0, 2.0, size=T_PASOS)

# --- 3. INICIALIZACIÓN Y BUCLE DEL FILTRO ---
filtro = ParticleFilter(num_particulas=1000, varianza_proceso=0.1, ancho_ruido_medicion=2.0)
historial_estimaciones = []

for t in range(T_PASOS):
    if t > 0:
        # a) Fase de Predicción
        filtro.predecir(velocidad=VELOCIDAD_REAL, dt=DT)
    
    # b) Fase de Actualización
    filtro.actualizar(medicion=mediciones[t])
    
    # c) Obtener la estimación del estado actual
    historial_estimaciones.append(filtro.estimar())
    
    # d) Fase de Remuestreo
    filtro.remuestrear()

# --- 4. VISUALIZACIÓN ---
plt.figure(figsize=(12, 6))
plt.plot(posicion_real, label='Posición Real (Verdad Oculta)', color='green', linewidth=3)
plt.scatter(range(T_PASOS), mediciones, label='Mediciones Ruidosas', color='red', alpha=0.5, marker='.')
plt.plot(historial_estimaciones, label='Estimación del Filtro de Partículas', color='blue', linestyle='--', linewidth=2)
plt.title('Seguimiento con Filtro de Partículas')
plt.xlabel('Paso de Tiempo')
plt.ylabel('Posición')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.show()