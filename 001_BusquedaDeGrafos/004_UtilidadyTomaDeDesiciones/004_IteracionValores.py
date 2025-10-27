# =========================================================================
# Solucionador de MDP con Iteración de Valores (Versión Orientada a Objetos)
# Problema: Encontrar el camino óptimo en un mundo de rejilla.
# =========================================================================

import numpy as np

class MDPSolver:
    """
    Encapsula la definición de un Proceso de Decisión de Markov (MDP) y lo
    resuelve usando el algoritmo de Iteración de Valores para encontrar la
    función de valor y la política óptimas.
    """
    def __init__(self, estados, acciones, transiciones, recompensas, gamma=0.9, epsilon=1e-3):
        self.estados = estados
        self.acciones = acciones
        self.transiciones = transiciones
        self.recompensas = recompensas
        self.gamma = gamma  # Factor de descuento
        self.epsilon = epsilon # Criterio de convergencia
        
        # Inicializar los valores de todos los estados a 0.
        self.valores = {s: 0.0 for s in self.estados}

    def solve(self):
        """
        Ejecuta el algoritmo de Iteración de Valores hasta la convergencia.
        """
        iteracion = 0
        while True:
            iteracion += 1
            delta = 0  # El cambio máximo en los valores en esta iteración.
            
            # Crear una copia para los nuevos valores calculados.
            nuevos_valores = self.valores.copy()

            for estado in self.estados:
                valor_antiguo = self.valores[estado]
                
                # --- Actualización de Bellman ---
                # V(s) = R(s) + γ * max_a Σ [ P(s'|s,a) * V(s') ]
                # Se calcula el valor esperado para cada acción posible desde el estado actual.
                valores_por_accion = []
                for accion in self.acciones:
                    estado_siguiente = self.transiciones[estado][accion]
                    # En este caso determinista, P(s'|s,a) es 1.
                    valor_esperado = self.gamma * self.valores[estado_siguiente]
                    valores_por_accion.append(valor_esperado)
                
                # El nuevo valor del estado es su recompensa intrínseca más el
                # valor máximo que se puede obtener al tomar la mejor acción.
                nuevos_valores[estado] = self.recompensas[estado] + max(valores_por_accion)
                
                # Actualizar el cambio máximo para el criterio de parada.
                delta = max(delta, abs(nuevos_valores[estado] - valor_antiguo))
            
            # Actualizar la tabla de valores para la siguiente iteración.
            self.valores = nuevos_valores

            # Criterio de parada: si los valores han dejado de cambiar significativamente.
            if delta < self.epsilon:
                print(f"\nConvergencia alcanzada en {iteracion} iteraciones.")
                break
        
        return self._extraer_politica()

    def _extraer_politica(self):
        """
        Calcula la política óptima (la mejor acción a tomar en cada estado)
        basándose en la función de valor ya calculada.
        """
        politica = {}
        for estado in self.estados:
            mejor_accion = None
            mejor_valor = -np.inf
            
            for accion in self.acciones:
                estado_siguiente = self.transiciones[estado][accion]
                valor_accion = self.gamma * self.valores[estado_siguiente]
                
                if valor_accion > mejor_valor:
                    mejor_valor = valor_accion
                    mejor_accion = accion
            
            politica[estado] = mejor_accion
        
        # El estado terminal no tiene una acción saliente.
        politica['S3'] = 'TERMINAL'
        return self.valores, politica

# --- 1. DEFINICIÓN DEL PROBLEMA ---
ESTADOS_MDP = ['S0', 'S1', 'S2', 'S3']
ACCIONES_MDP = ['N', 'S', 'E', 'O']

# Transiciones deterministas: T(estado, accion) -> estado_siguiente
TRANSICIONES_MDP = {
    'S0': {'N': 'S2', 'E': 'S1', 'S': 'S0', 'O': 'S0'},
    'S1': {'N': 'S3', 'O': 'S0', 'S': 'S1', 'E': 'S1'},
    'S2': {'E': 'S3', 'S': 'S0', 'N': 'S2', 'O': 'S2'},
    'S3': {'N': 'S3', 'S': 'S3', 'E': 'S3', 'O': 'S3'} # Estado absorbente
}

# Recompensas: Solo el estado S3 (meta) tiene una recompensa positiva.
RECOMPENSAS_MDP = {'S0': 0, 'S1': 0, 'S2': 0, 'S3': 10}

# --- 2. EJECUCIÓN ---
# Se crea una instancia del solucionador con la definición del problema.
solucionador = MDPSolver(
    estados=ESTADOS_MDP,
    acciones=ACCIONES_MDP,
    transiciones=TRANSICIONES_MDP,
    recompensas=RECOMPENSAS_MDP
)

# Se resuelve el MDP.
valores_optimos, politica_optima = solucionador.solve()

# --- 3. RESULTADOS ---
print("=" * 50)
print("Función de Valor Óptima V*(s):")
# Imprime los valores formateados
for estado, valor in valores_optimos.items():
    print(f"  V({estado}) = {valor:.3f}")

print("\nPolítica Óptima π*(s):")
# Imprime la política de forma clara
for estado, accion in politica_optima.items():
    print(f"  En {estado}, tomar acción: {accion}")