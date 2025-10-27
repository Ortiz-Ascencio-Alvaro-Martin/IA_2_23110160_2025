# =========================================================================
# Simulación de una Cadena de Markov (Versión Simplificada con NumPy)
# =========================================================================

import numpy as np

def simular_clima_markov(dias, estado_inicial, transiciones):
    """
    Simula una secuencia de estados del clima usando una Cadena de Markov.
    """
    # 1. Preparar el modelo para un acceso rápido.
    estados = list(transiciones.keys())
    matriz_T = np.array([list(transiciones[estado].values()) for estado in estados])
    
    # 2. Simulación
    historia_estados = [estado_inicial]
    estado_actual = estado_inicial
    
    for _ in range(dias - 1):
        # El índice del estado actual en nuestra lista de estados.
        indice_actual = estados.index(estado_actual)
        
        # Se elige el siguiente estado usando las probabilidades de la fila correspondiente.
        estado_siguiente = np.random.choice(estados, p=matriz_T[indice_actual])
        
        historia_estados.append(estado_siguiente)
        estado_actual = estado_siguiente
        
    return historia_estados

# --- 1. Definición del Modelo ---
# La matriz de transición P(estado_siguiente | estado_actual).
MATRIZ_CLIMA = {
    'Soleado':  {'Soleado': 0.8, 'Nublado': 0.15, 'Lluvioso': 0.05},
    'Nublado':  {'Soleado': 0.2, 'Nublado': 0.6,  'Lluvioso': 0.2},
    'Lluvioso': {'Soleado': 0.1, 'Nublado': 0.3,  'Lluvioso': 0.6}
}

# --- 2. Ejecución ---
NUM_DIAS_SIMULADOS = 1000
ESTADO_DE_INICIO = 'Soleado'

print(f"--- Simulación de una Cadena de Markov para el Clima ({NUM_DIAS_SIMULADOS} días) ---")
historial = simular_clima_markov(NUM_DIAS_SIMULADOS, ESTADO_DE_INICIO, MATRIZ_CLIMA)

print(f"Primeros 10 días de la simulación: {' -> '.join(historial[:10])}")

# --- 3. Análisis de Resultados ---
# Se cuenta la frecuencia de cada estado para observar la distribución a largo plazo.
frecuencias = {
    'Soleado': historial.count('Soleado') / NUM_DIAS_SIMULADOS,
    'Nublado': historial.count('Nublado') / NUM_DIAS_SIMULADOS,
    'Lluvioso': historial.count('Lluvioso') / NUM_DIAS_SIMULADOS
}

print("\n" + "="*50)
print("Distribución de Estados a Largo Plazo (Frecuencias):")
for estado, frec in frecuencias.items():
    print(f"  - {estado}: {frec:.2%}")

print("\nConclusión: Después de muchos días, la probabilidad de que un día cualquiera sea soleado, nublado o lluvioso tiende a estabilizarse.")