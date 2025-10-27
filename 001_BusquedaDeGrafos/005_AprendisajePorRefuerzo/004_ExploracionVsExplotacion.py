# =========================================================================
# Dilema del Bandido Multibrazo con Epsilon-Greedy (Versión Orientada a Objetos)
# Objetivo: Un agente debe aprender cuál es la mejor máquina (brazo) para
# maximizar su recompensa a largo plazo.
# =========================================================================

import random
import numpy as np

class EntornoBandit:
    """
    Representa el conjunto de máquinas tragamonedas (los "brazos" o "bandidos").
    Conoce la verdadera probabilidad de éxito de cada una.
    """
    def __init__(self, probabilidades_reales):
        self.palancas = probabilidades_reales

    def jalar_palanca(self, id_palanca):
        """
        Simula la acción de jalar una palanca y devuelve una recompensa.
        """
        # Se genera un número aleatorio; si es menor que la probabilidad de la
        # palanca, se considera un éxito (recompensa = 1).
        if random.random() < self.palancas[id_palanca]:
            return 1
        return 0

class AgenteEpsilonGreedy:
    """
    Representa al agente que aprende. Mantiene un registro de sus estimaciones
    y utiliza la estrategia epsilon-greedy para equilibrar exploración y explotación.
    """
    def __init__(self, num_palancas, epsilon):
        self.epsilon = epsilon  # Tasa de exploración (ε)
        self.num_palancas = num_palancas
        
        # El "cerebro" del agente:
        # q_estimado: La recompensa promedio que el agente CREE que da cada palanca.
        # n_conteo: El número de veces que el agente ha jalado cada palanca.
        self.q_estimado = np.zeros(num_palancas)
        self.n_conteo = np.zeros(num_palancas)

    def elegir_accion(self):
        """
        Decide qué palanca jalar basándose en la estrategia epsilon-greedy.
        """
        if random.random() < self.epsilon:
            # 1. Exploración: Elegir una palanca al azar.
            return random.randint(0, self.num_palancas - 1)
        else:
            # 2. Explotación: Elegir la palanca que actualmente tiene la mejor estimación.
            return np.argmax(self.q_estimado)

    def aprender(self, id_palanca, recompensa):
        """
        Actualiza el conocimiento del agente (sus estimaciones) basándose en
        la recompensa obtenida.
        """
        # Se incrementa el contador para la palanca que se jaló.
        self.n_conteo[id_palanca] += 1
        n = self.n_conteo[id_palanca]
        
        # Se actualiza la estimación de la recompensa promedio de forma incremental.
        # Q_nuevo = Q_viejo + (1/n) * (Recompensa_obtenida - Q_viejo)
        error = recompensa - self.q_estimado[id_palanca]
        self.q_estimado[id_palanca] += (1 / n) * error

# --- 1. CONFIGURACIÓN DE LA SIMULACIÓN ---
# Probabilidades reales de cada máquina (el agente no las conoce).
PROBABILIDADES_MAQUINAS = [0.4, 0.6, 0.5] # La máquina 1 es la mejor.
NUM_PALANCAS = len(PROBABILIDADES_MAQUINAS)
PASOS_TOTALES = 1000
TASA_EXPLORACION = 0.1

# --- 2. CREACIÓN DEL ENTORNO Y DEL AGENTE ---
entorno = EntornoBandit(PROBABILIDADES_MAQUINAS)
agente = AgenteEpsilonGreedy(num_palancas=NUM_PALANCAS, epsilon=TASA_EXPLORACION)

# --- 3. BUCLE PRINCIPAL DE SIMULACIÓN ---
recompensa_acumulada = 0
for _ in range(PASOS_TOTALES):
    # 1. El agente elige una acción (una palanca para jalar).
    palanca_elegida = agente.elegir_accion()
    
    # 2. El entorno responde con una recompensa.
    recompensa = entorno.jalar_palanca(palanca_elegida)
    
    # 3. El agente aprende de la experiencia.
    agente.aprender(palanca_elegida, recompensa)
    
    # Se acumula la recompensa.
    recompensa_acumulada += recompensa

# --- 4. RESULTADOS FINALES ---
print(f"--- Simulación del Bandido Epsilon-Greedy (ε={TASA_EXPLORACION}) ---")
print(f"Recompensa total obtenida en {PASOS_TOTALES} pasos: {recompensa_acumulada}")
print("-" * 50)
print("Conocimiento Final del Agente:")
for i in range(NUM_PALANCAS):
    print(f"  - Máquina {i}: Estimación de Recompensa = {agente.q_estimado[i]:.4f}")
    print(f"    (Probabilidad real: {PROBABILIDADES_MAQUINAS[i]}, Jalada {int(agente.n_conteo[i])} veces)")

print("\nConclusión:")
palanca_optima_aprendida = np.argmax(agente.q_estimado)
palanca_optima_real = np.argmax(PROBABILIDADES_MAQUINAS)

if palanca_optima_aprendida == palanca_optima_real:
    print(f"¡Éxito! El agente identificó correctamente la mejor máquina (la #{palanca_optima_real}).")
else:
    print(f"El agente creyó que la mejor máquina era la #{palanca_optima_aprendida}, pero en realidad era la #{palanca_optima_real}.")