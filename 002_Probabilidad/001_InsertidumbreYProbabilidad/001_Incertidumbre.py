# =========================================================================
# Bandido Multibrazo con Inicialización Optimista (Versión Orientada a Objetos)
# Objetivo: Forzar la exploración inicial al asumir que todas las opciones
# son mejores de lo que realmente son.
# =========================================================================

import random
import numpy as np

class EntornoBandit:
    """
    Representa el conjunto de máquinas tragamonedas (los "brazos").
    Conoce la verdadera probabilidad de éxito de cada una.
    """
    def __init__(self, probabilidades_reales):
        self.palancas = probabilidades_reales

    def jalar_palanca(self, id_palanca):
        """
        Simula la acción de jalar una palanca y devuelve una recompensa (0 o 1).
        """
        return 1 if random.random() < self.palancas[id_palanca] else 0

class AgenteOptimista:
    """
    Representa un agente que utiliza la inicialización optimista para explorar.
    Siempre elige la mejor opción actual (es "greedy"), pero su optimismo inicial
    lo obliga a probar todas las opciones hasta que sus estimaciones se ajusten.
    """
    def __init__(self, num_palancas, valor_inicial_q, tasa_aprendizaje):
        self.alpha = tasa_aprendizaje
        # El "cerebro" del agente se inicializa con un valor muy optimista.
        self.q_estimado = np.full(num_palancas, valor_inicial_q, dtype=float)

    def elegir_accion(self):
        """
        Siempre elige la palanca que actualmente tiene la mejor estimación.
        La exploración es implícita, no aleatoria.
        """
        return np.argmax(self.q_estimado)

    def aprender(self, id_palanca, recompensa):
        """
        Actualiza la estimación de la recompensa para la palanca seleccionada.
        """
        # Q_nuevo = Q_viejo + α * (Recompensa - Q_viejo)
        error = recompensa - self.q_estimado[id_palanca]
        self.q_estimado[id_palanca] += self.alpha * error

# --- 1. CONFIGURACIÓN DE LA SIMULACIÓN ---
PROBABILIDADES_MAQUINAS = [0.4, 0.6, 0.5] # La máquina 1 es la mejor
PASOS_TOTALES = 500
VALOR_INICIAL_OPTIMISTA = 5.0 # Un valor deliberadamente alto
TASA_APRENDIZAJE = 0.1

# --- 2. CREACIÓN DEL ENTORNO Y DEL AGENTE ---
entorno = EntornoBandit(PROBABILIDADES_MAQUINAS)
agente = AgenteOptimista(
    num_palancas=len(PROBABILIDADES_MAQUINAS),
    valor_inicial_q=VALOR_INICIAL_OPTIMISTA,
    tasa_aprendizaje=TASA_APRENDIZAJE
)

# --- 3. BUCLE PRINCIPAL DE SIMULACIÓN ---
conteo_de_jugadas = np.zeros(len(PROBABILIDADES_MAQUINAS))
print(f"--- Simulación con Inicialización Optimista (Q_inicial = {VALOR_INICIAL_OPTIMISTA}) ---")
print(f"Q Inicial: {agente.q_estimado}")

for _ in range(PASOS_TOTALES):
    # 1. El agente elige una acción de forma "greedy".
    palanca_elegida = agente.elegir_accion()
    conteo_de_jugadas[palanca_elegida] += 1