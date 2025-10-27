# =========================================================================
# Aprendizaje Pasivo por Diferencia Temporal (TD(0)) - Versión Procedural
# Objetivo: Estimar el valor V(s) de cada estado bajo una política fija.
# =========================================================================

import random
import numpy as np

def resolver_con_td_pasivo(politica, transiciones, parametros):
    """
    Ejecuta el algoritmo de aprendizaje TD(0) para estimar el valor de una política.
    """
    # 1. Inicializar la tabla de valores V(s) a cero.
    valores_v = {estado: 0.0 for estado in parametros['estados']}
    estado_terminal = 'S3'
    
    print("--- Iniciando aprendizaje TD(0) para una política fija ---")

    # 2. Bucle principal de episodios.
    for episodio in range(1, parametros['episodios'] + 1):
        
        # Cada episodio comienza en el estado inicial.
        estado = parametros['estado_inicial']
        
        # Simular una trayectoria hasta llegar al estado terminal.
        while estado != estado_terminal:
            estado_anterior = estado
            
            # 3. Observar la transición y la recompensa del mundo.
            estado_siguiente = transiciones[estado_anterior]
            
            if estado_siguiente == estado_terminal:
                recompensa = parametros['recompensa_meta']
            else:
                recompensa = parametros['recompensa_paso']

            # 4. Actualizar el conocimiento usando la regla TD(0).
            # Objetivo = R + γ * V(s')
            objetivo_td = recompensa + parametros['gamma'] * valores_v[estado_siguiente]
            # Error = Objetivo - V(s)
            error_td = objetivo_td - valores_v[estado_anterior]
            # V(s) <- V(s) + α * Error
            valores_v[estado_anterior] += parametros['alpha'] * error_td
            
            # Moverse al siguiente estado.
            estado = estado_siguiente

        # Imprimir el progreso periódicamente.
        if episodio % (parametros['episodios'] // 10) == 0 or episodio == 1:
            v_str = ', '.join([f'{s}={v:.4f}' for s, v in valores_v.items()])
            print(f"Episodio {episodio:04d}: {v_str}")
            
    return valores_v

# --- 1. CONFIGURACIÓN DEL PROBLEMA ---
# Agrupar todos los parámetros en un diccionario para mayor claridad.
PARAMETROS_MDP = {
    'estados': ['S0', 'S1', 'S2', 'S3'],
    'estado_inicial': 'S0',
    'alpha': 0.01,       # Tasa de aprendizaje
    'gamma': 0.8,        # Factor de descuento
    'episodios': 1000,
    'recompensa_paso': -1,
    'recompensa_meta': 10
}

# La política fija que el agente seguirá.
POLITICA_FIJA_MDP = {'S0': 'D', 'S1': 'D', 'S2': 'D', 'S3': None}

# Las transiciones deterministas del entorno.
TRANSICIONES_MDP = {'S0': 'S1', 'S1': 'S2', 'S2': 'S3'}

# --- 2. EJECUCIÓN DEL APRENDIZAJE ---
valores_estimados = resolver_con_td_pasivo(POLITICA_FIJA_MDP, TRANSICIONES_MDP, PARAMETROS_MDP)

# --- 3. RESULTADOS FINALES ---
print("\n" + "="*60)
print("VALOR FINAL ESTIMADO V^π(s):")
print(f"  V(S0): {valores_estimados['S0']:.4f} (Teórico: 4.58)")
print(f"  V(S1): {valores_estimados['S1']:.4f} (Teórico: 6.20)")
print(f"  V(S2): {valores_estimados['S2']:.4f} (Teórico: 8.00)")
print(f"  V(S3): {valores_estimados['S3']:.4f} (El valor del estado terminal no se actualiza y permanece en 0)")