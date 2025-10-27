# =========================================================================
# Decodificador de Habla con HMM y Viterbi (Versión Orientada a Objetos)
# =========================================================================

import numpy as np

class SpeechDecoder:
    """
    Encapsula un conjunto de Modelos Ocultos de Markov (uno por palabra) y
    utiliza el algoritmo de Viterbi para decodificar la palabra más probable
    a partir de una secuencia de observaciones acústicas.
    """

    def __init__(self, modelos_de_palabras):
        """
        Inicializa el decodificador con un diccionario de modelos, donde cada
        clave es una palabra y el valor es su modelo HMM.
        """
        self.modelos = modelos_de_palabras
        self.obs_map = {'Fuerte': 0, 'Suave': 1}

    def _calcular_verosimilitud_viterbi(self, observaciones, modelo):
        """
        Calcula la probabilidad de la secuencia de observaciones dada un
        modelo de palabra específico, usando el algoritmo de Viterbi.
        Retorna la probabilidad del camino más probable.
        """
        T = len(observaciones)
        n_estados = modelo['A'].shape[0]
        
        delta = np.zeros((T, n_estados))
        
        # Inicialización
        obs_idx_0 = self.obs_map[observaciones[0]]
        delta[0, :] = modelo['pi'] * modelo['B'][:, obs_idx_0]

        # Recursión
        for t in range(1, T):
            obs_idx_t = self.obs_map[observaciones[t]]
            for j in range(n_estados):
                trans_probs = delta[t-1, :] * modelo['A'][:, j]
                delta[t, j] = np.max(trans_probs) * modelo['B'][j, obs_idx_t]

        # El resultado es la probabilidad del camino más probable al final.
        return np.max(delta[T-1, :])

    def decodificar(self, observaciones):
        """
        Compara la secuencia de observaciones con todos los modelos de palabras
        y devuelve la palabra cuyo modelo asigna la mayor probabilidad.
        """
        mejor_palabra = None
        mejor_probabilidad = -1.0

        # Iterar sobre cada palabra y su modelo HMM.
        for palabra, modelo in self.modelos.items():
            # Calcular qué tan "probable" es esta palabra dado el audio.
            probabilidad = self._calcular_verosimilitud_viterbi(observaciones, modelo)
            
            # Si esta palabra es más probable que la mejor encontrada hasta ahora, se actualiza.
            if probabilidad > mejor_probabilidad:
                mejor_probabilidad = probabilidad
                mejor_palabra = palabra
                
        return mejor_palabra, mejor_probabilidad

# --- 1. DEFINICIÓN DE LOS MODELOS HMM (Uno para cada palabra) ---
# Modelo base compartido
PI_BASE = np.array([1.0, 0.0, 0.0, 0.0])
A_BASE = np.array([
    [0.0, 1.0, 0.0, 0.0], # T/L -> o
    [0.0, 0.0, 1.0, 0.0], # o   -> m
    [0.0, 0.0, 0.0, 1.0], # m   -> a
    [0.0, 0.0, 0.0, 0.0]  # a   -> fin
])

# Modelo para "Toma" (el fonema inicial 'T' es 'Fuerte')
MODELO_TOMA = {
    'pi': PI_BASE,
    'A': A_BASE,
    'B': np.array([
        [0.8, 0.2], # P(Obs | 'T') -> [Fuerte, Suave]
        [0.5, 0.5], # P(Obs | 'o')
        [0.4, 0.6], # P(Obs | 'm')
        [0.3, 0.7]  # P(Obs | 'a')
    ])
}

# Modelo para "Loma" (el fonema inicial 'L' es 'Suave')
MODELO_LOMA = {
    'pi': PI_BASE,
    'A': A_BASE,
    'B': np.array([
        [0.2, 0.8], # P(Obs | 'L') -> [Fuerte, Suave]
        [0.5, 0.5], # P(Obs | 'o')
        [0.4, 0.6], # P(Obs | 'm')
        [0.3, 0.7]  # P(Obs | 'a')
    ])
}

# --- 2. EJECUCIÓN DEL DECODIFICADOR ---
# Se crea una instancia del decodificador con los modelos que conoce.
decodificador = SpeechDecoder({'Toma': MODELO_TOMA, 'Loma': MODELO_LOMA})

# Casos de prueba
AUDIO_CASO_1 = ['Suave', 'Suave', 'Suave', 'Suave'] # Debería ser "Loma"
AUDIO_CASO_2 = ['Fuerte', 'Suave', 'Suave', 'Suave'] # Debería ser "Toma"

# Decodificar ambos audios.
palabra_1, prob_1 = decodificador.decodificar(AUDIO_CASO_1)
palabra_2, prob_2 = decodificador.decodificar(AUDIO_CASO_2)

# --- 3. RESULTADOS ---
print("--- Decodificación de Habla con Modelos Competidores ---")
print(f"Observación 1: {AUDIO_CASO_1}")
print(f"  ➡️  Palabra Decodificada: '{palabra_1}' (con probabilidad de camino {prob_1:.2e})")
print("-" * 50)
print(f"Observación 2: {AUDIO_CASO_2}")
print(f"  ➡️  Palabra Decodificada: '{palabra_2}' (con probabilidad de camino {prob_2:.2e})")