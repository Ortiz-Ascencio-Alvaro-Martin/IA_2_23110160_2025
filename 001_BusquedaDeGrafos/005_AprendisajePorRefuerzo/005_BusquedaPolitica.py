# =========================================================================
# Búsqueda de Política con REINFORCE (Versión Orientada a Objetos)
# Objetivo: Aprender una política estocástica que maximice la recompensa
# ajustando un parámetro (theta) mediante el ascenso por gradiente.
# =========================================================================

import random
import numpy as np

class AgenteREINFORCE:
    """
    Representa un agente que aprende una política usando el algoritmo REINFORCE.
    El agente ajusta su parámetro de política 'theta' para favorecer acciones
    que conducen a mayores recompensas.
    """

    def __init__(self, tasa_aprendizaje):
        self.alpha = tasa_aprendizaje
        # El "cerebro" del agente es un único parámetro que define su política.
        self.theta = 0.0

    def _calcular_prob_politica(self):
        """
        Calcula la probabilidad de tomar la acción 'Derecha' usando la
        función sigmoide, que mapea theta a una probabilidad entre 0 y 1.
        """
        return 1 / (1 + np.exp(-self.theta))

    def elegir_accion(self):
        """
        Selecciona una acción ('Derecha' o 'Izquierda') basándose en la
        probabilidad actual dictada por su política.
        """
        prob_derecha = self._calcular_prob_politica()
        if random.random() < prob_derecha:
            return 'Derecha'
        return 'Izquierda'

    def aprender(self, accion_tomada, recompensa_obtenida):
        """
        Actualiza el parámetro de la política (theta) usando la regla de REINFORCE.
        """
        prob_derecha = self._calcular_prob_politica()

        # 1. Calcular el "score" del gradiente (∇log π).
        # Este término indica en qué dirección se debe mover theta para
        # aumentar la probabilidad de la acción que se tomó.
        if accion_tomada == 'Derecha':
            gradiente_log_prob = 1 - prob_derecha
        else: # 'Izquierda'
            gradiente_log_prob = -prob_derecha

        # 2. Aplicar la actualización de REINFORCE.
        # θ ← θ + α * G * ∇log(π)
        # El ajuste se pondera por la recompensa (G): los ajustes son más grandes
        # para acciones que llevaron a recompensas altas.
        ajuste = self.alpha * recompensa_obtenida * gradiente_log_prob
        self.theta += ajuste

# --- 1. CONFIGURACIÓN DE LA SIMULACIÓN ---
TASA_APRENDIZAJE = 0.1
EPISODIOS = 500

# --- 2. CREACIÓN DEL AGENTE ---
agente = AgenteREINFORCE(tasa_aprendizaje=TASA_APRENDIZAJE)

# --- 3. BUCLE PRINCIPAL DE APRENDIZAJE ---
print("--- Iniciando Búsqueda de Política con REINFORCE ---")

for episodio in range(EPISODIOS):
    # 1. El agente elige una acción según su política actual.
    accion = agente.elegir_accion()
    
    # 2. El entorno responde con una recompensa (el retorno total G).
    # En este problema simple, la recompensa es 1 si va a la derecha, 0 si no.
    recompensa = 1 if accion == 'Derecha' else 0
    
    # 3. El agente aprende de la experiencia, ajustando su política.
    agente.aprender(accion, recompensa)
    
    # Imprimir el progreso periódicamente.
    if episodio % (EPISODIOS / 10) == 0:
        prob_actual = agente._calcular_prob_politica()
        print(f"Episodio {episodio:03d}: θ={agente.theta:.4f} | Prob(Derecha)={prob_actual:.4f}")

# --- 4. RESULTADOS FINALES ---
probabilidad_final = agente._calcular_prob_politica()

print("\n" + "="*50)
print("Resultados Finales del Aprendizaje:")
print(f"  Parámetro de política final (θ): {agente.theta:.4f}")
print(f"  Probabilidad final de 'Derecha' (π*): {probabilidad_final:.4f}")
print("="*50)

if probabilidad_final > 0.95:
    print("Conclusión: La política del agente ha convergido exitosamente a la acción óptima.")
else:
    print("Conclusión: La política no convergió completamente a la acción óptima.")
    #