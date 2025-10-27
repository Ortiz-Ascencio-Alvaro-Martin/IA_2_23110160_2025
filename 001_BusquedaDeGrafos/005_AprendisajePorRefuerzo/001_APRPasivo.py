# =========================================================================
# Aprendizaje Pasivo por Diferencia Temporal (TD(0)) - Versión Orientada a Objetos
# Objetivo: Estimar el valor V(s) de cada estado bajo una política fija.
# =========================================================================

import random
import numpy as np

class EntornoSimple:
    """
    Representa el mundo en el que actúa el agente. Conoce las reglas,
    transiciones y recompensas.
    """
    def __init__(self, transiciones, recompensa_paso, recompensa_meta, estado_meta):
        self.transiciones = transiciones
        self.recompensa_paso = recompensa_paso
        self.recompensa_meta = recompensa_meta
        self.estado_meta = estado_meta

    def obtener_transicion(self, estado):
        """
        Dado un estado, devuelve el siguiente estado y la recompensa obtenida.
        """
        estado_siguiente = self.transiciones[estado]
        
        if estado_siguiente == self.estado_meta:
            recompensa = self.recompensa_meta
        else:
            recompensa = self.recompensa_paso
            
        return estado_siguiente, recompensa

class AgentePasivoTD:
    """
    Representa un agente que sigue una política fija y aprende el valor de los
    estados usando el algoritmo TD(0).
    """
    def __init__(self, estados, politica, alpha, gamma):
        self.politica = politica
        self.tasa_aprendizaje = alpha # α
        self.factor_descuento = gamma  # γ
        # El agente inicializa su conocimiento (la función de valor) en cero.
        self.valores_v = {s: 0.0 for s in estados}
        self.estado_terminal = 'S3'

    def aprender_un_episodio(self, entorno, estado_inicial='S0'):
        """
        Simula una trayectoria completa (un episodio) desde un estado inicial
        hasta un estado terminal, actualizando los valores en cada paso.
        """
        estado = estado_inicial
        while estado != self.estado_terminal:
            estado_anterior = estado
            
            # 1. El agente observa el mundo para obtener la transición.
            estado_siguiente, recompensa = entorno.obtener_transicion(estado_anterior)
            
            # 2. El agente actualiza su conocimiento con la nueva experiencia.
            # --- Actualización TD(0) ---
            # Objetivo TD = Recompensa + γ * V(EstadoSiguiente)
            valor_estado_siguiente = self.valores_v[estado_siguiente]
            objetivo_td = recompensa + self.factor_descuento * valor_estado_siguiente
            
            # Error TD = Objetivo - V(EstadoActual)
            error_td = objetivo_td - self.valores_v[estado_anterior]
            
            # V(s) <- V(s) + α * error
            self.valores_v[estado_anterior] += self.tasa_aprendizaje * error_td
            
            # 3. El agente se mueve al siguiente estado.
            estado = estado_siguiente

# --- 1. CONFIGURACIÓN DEL PROBLEMA ---
ESTADOS_MDP = ['S0', 'S1', 'S2', 'S3']
POLITICA_FIJA = {'S0': 'D', 'S1': 'D', 'S2': 'D', 'S3': None}
TRANSICIONES_FIJAS = {'S0': 'S1', 'S1': 'S2', 'S2': 'S3'}
PARAMETROS = {
    'alpha': 0.01,
    'gamma': 0.8,
    'episodios': 1000,
    'recompensa_paso': -1,
    'recompensa_meta': 10
}

# --- 2. CREACIÓN DEL ENTORNO Y DEL AGENTE ---
entorno = EntornoSimple(TRANSICIONES_FIJAS, PARAMETROS['recompensa_paso'], PARAMETROS['recompensa_meta'], 'S3')
agente = AgentePasivoTD(ESTADOS_MDP, POLITICA_FIJA, PARAMETROS['alpha'], PARAMETROS['gamma'])

# --- 3. BUCLE PRINCIPAL DE APRENDIZAJE ---
print("--- Iniciando aprendizaje TD(0) para una política fija ---")

for episodio in range(1, PARAMETROS['episodios'] + 1):
    agente.aprender_un_episodio(entorno)
    
    if episodio % (PARAMETROS['episodios'] // 10) == 0 or episodio == 1:
        v_str = ', '.join([f'{s}={v:.4f}' for s, v in agente.valores_v.items()])
        print(f"Episodio {episodio:04d}: {v_str}")

# --- 4. RESULTADOS FINALES ---
print("\n" + "="*60)
print("VALOR FINAL ESTIMADO V^π(s) por el agente:")
print(f"  V(S0): {agente.valores_v['S0']:.4f} (Teórico: 4.58)")
print(f"  V(S1): {agente.valores_v['S1']:.4f} (Teórico: 6.20)")
print(f"  V(S2): {agente.valores_v['S2']:.4f} (Teórico: 8.00)")
print(f"  V(S3): {agente.valores_v['S3']:.4f} (El valor del estado terminal no se actualiza y permanece en 0)")