# =========================================================================
# Evaluación de Políticas en un MDP (Versión Orientada a Objetos)
# Propósito: Calcular el valor a largo plazo V(s) de seguir una política fija.
# =========================================================================

class EvaluadorDePoliticas:
    """
    Encapsula un Proceso de Decisión de Markov (MDP) y calcula el valor
    de una política específica usando la Evaluación Iterativa de Políticas.
    """

    def __init__(self, mdp_definicion, umbral_convergencia=1e-4):
        """
        Inicializa el evaluador con la definición del MDP.
        """
        self.estados = mdp_definicion['estados']
        self.transiciones = mdp_definicion['transiciones']
        self.recompensas = mdp_definicion['recompensas']
        self.gamma = mdp_definicion['gamma']
        self.theta = umbral_convergencia # Criterio para detener la evaluación.

    def evaluar(self, politica):
        """
        Calcula la función de valor V(s) para una política dada hasta la convergencia.
        Este es el corazón del algoritmo de Evaluación Iterativa de Políticas.
        """
        # 1. Se inicializa el valor de todos los estados en 0.
        V = {s: 0.0 for s in self.estados}
        iteracion = 0
        
        while True:
            iteracion += 1
            delta = 0  # El cambio máximo en los valores en esta pasada.
            
            for s in self.estados:
                valor_antiguo = V[s]
                
                # Para el estado terminal, el valor es simplemente su recompensa.
                if s == 'S3':
                    V[s] = self.recompensas['S3']
                    continue
                
                # 2. Se obtiene la acción fija que dicta la política para el estado actual.
                accion_fija = politica[s]
                
                # --- 3. Aplicación de la Ecuación de Bellman para V^π ---
                # V(s) = R(s) + γ * Σ [ P(s'|s, π(s)) * V_k(s') ]
                # Se calcula el valor futuro esperado sumando los valores de todos los
                # posibles estados siguientes, ponderados por su probabilidad.
                valor_futuro_esperado = 0
                for estado_siguiente, probabilidad in self.transiciones[s][accion_fija].items():
                    valor_futuro_esperado += probabilidad * V[estado_siguiente]
                
                # Se actualiza el valor del estado actual.
                V[s] = self.recompensas[s] + self.gamma * valor_futuro_esperado
                
                # 4. Se registra el cambio para verificar la convergencia.
                delta = max(delta, abs(valor_antiguo - V[s]))
            
            valores_str = ', '.join([f'{estado}={valor:.3f}' for estado, valor in V.items()])
            print(f"Iteración {iteracion:02d}: {valores_str}, Delta={delta:.4f}")
            
            # 5. Si los valores ya no cambian significativamente, hemos convergido.
            if delta < self.theta:
                break
                
        return V

# --- 1. DEFINICIÓN DEL MDP (agrupado en un diccionario) ---
MDP_PROBLEMA = {
    'estados': ['S0', 'S1', 'S2', 'S3'],
    'gamma': 0.9,
    'recompensas': {'S0': 0, 'S1': 0, 'S2': 0, 'S3': 10},
    'transiciones': {
        'S0': {
            'E': {'S1': 0.8, 'S2': 0.2},
            'N': {'S2': 0.8, 'S1': 0.2}
        },
        'S1': {
            'E': {'S1': 1.0},
            'N': {'S3': 0.8, 'S1': 0.2}
        },
        'S2': {
            'E': {'S3': 0.8, 'S0': 0.2},
            'N': {'S2': 1.0}
        },
        'S3': { # Estado terminal
            'E': {'S3': 1.0},
            'N': {'S3': 1.0}
        }
    }
}

# --- 2. POLÍTICA A EVALUAR ---
# Una política simple: intentar siempre ir al Este.
POLITICA_A_EVALUAR = {'S0': 'E', 'S1': 'E', 'S2': 'E', 'S3': 'E'}

# --- 3. EJECUCIÓN ---
# Se crea una instancia del evaluador con la definición del problema.
evaluador = EvaluadorDePoliticas(MDP_PROBLEMA)

print(f"--- Evaluando la Política π = {POLITICA_A_EVALUAR} ---")
# Se llama al método para evaluar la política específica.
valores_finales = evaluador.evaluar(POLITICA_A_EVALUAR)

print("\n" + "="*50)
print("Resultado Final de la Evaluación:")
print("\nFunción de Valor V^π(s) para la política dada:")
for estado, valor in valores_finales.items():
    print(f"  El valor a largo plazo de estar en {estado} es: {valor:.3f}")
    #