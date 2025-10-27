# =========================================================================
# Actualización de Creencias en un POMDP (Versión Orientada a Objetos)
# Problema: Un robot infiere si una habitación está limpia o sucia
# basándose en observaciones ruidosas.
# =========================================================================

class AgentePOMDP:
    """
    Representa un agente que mantiene un estado de creencia sobre un
    entorno parcialmente observable y lo actualiza basándose en sus
    acciones y observaciones.
    """

    def __init__(self, modelo_pomdp, creencia_inicial):
        """
        Inicializa el agente con su conocimiento del mundo y su creencia inicial.
        """
        self.estados = modelo_pomdp['estados']
        self.transiciones = modelo_pomdp['transiciones']
        self.observaciones = modelo_pomdp['observaciones']
        self.creencia = creencia_inicial # El "mapa mental" actual del agente.

    def actualizar_creencia(self, accion, observacion):
        """
        Realiza una actualización de creencia completa usando el filtro de Bayes.
        """
        # --- 1. Paso de Predicción ---
        # El agente predice cuál será el nuevo estado antes de considerar la observación.
        # P(s') = Σ [ P(s'|s, a) * b(s) ] para cada estado s del pasado.
        prediccion = {s_prime: 0 for s_prime in self.estados}
        for s_prime in self.estados:
            suma_ponderada = sum(
                self.transiciones[s][s_prime] * self.creencia[s]
                for s in self.estados
            )
            prediccion[s_prime] = suma_ponderada
            
        # --- 2. Paso de Actualización ---
        # El agente corrige su predicción usando la nueva evidencia (observación).
        # b'(s') = α * P(o|s') * P(s')
        b_nueva_sin_normalizar = {}
        for s_prime in self.estados:
            prob_observacion = self.observaciones[observacion][s_prime]
            b_nueva_sin_normalizar[s_prime] = prob_observacion * prediccion[s_prime]
            
        # Se calcula el factor de normalización (α) para que las probabilidades sumen 1.
        alfa = sum(b_nueva_sin_normalizar.values())
        
        # Se actualiza la creencia interna del agente.
        self.creencia = {s: v / alfa for s, v in b_nueva_sin_normalizar.items()}

# --- 1. DEFINICIÓN DEL MODELO DEL MUNDO (POMDP) ---
MODELO_ROBOT = {
    'estados': ['Limpio', 'Sucio'],
    'transiciones': { # P(s' | s, a='Esperar')
        'Limpio': {'Limpio': 0.9, 'Sucio': 0.1},
        'Sucio': {'Limpio': 0.2, 'Sucio': 0.8}
    },
    'observaciones': { # P(o | s')
        'OK': {'Limpio': 0.7, 'Sucio': 0.1},
        'RUIDO': {'Limpio': 0.3, 'Sucio': 0.9}
    }
}

# --- 2. SIMULACIÓN ---
creencia_inicial = {'Limpio': 0.5, 'Sucio': 0.5}

# Se crea una instancia del agente con su conocimiento del mundo.
robot = AgentePOMDP(MODELO_ROBOT, creencia_inicial)

print("--- Simulación de Creencia del Agente POMDP ---")
print(f"Creencia Inicial b0: {robot.creencia}")
print("=" * 50)

# Una secuencia de observaciones que el robot recibe.
secuencia_observaciones = ['OK', 'RUIDO', 'OK']
accion_constante = 'Esperar'

for i, obs in enumerate(secuencia_observaciones):
    # El agente actualiza su creencia interna con cada nueva observación.
    robot.actualizar_creencia(accion_constante, obs)
    
    print(f"Paso {i+1}: Acción='{accion_constante}', Observación='{obs}'")
    print(f"  -> Nueva Creencia b{i+1}: ", end="")
    creencia_str = [f"P({s})={p:.4f}" for s, p in robot.creencia.items()]
    print(", ".join(creencia_str))