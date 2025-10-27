# =========================================================================
# Solucionador de MDP con Iteración de Políticas (Versión Orientada a Objetos)
# =========================================================================

import numpy as np

class PolicyIterationSolver:
    """
    Encapsula un Proceso de Decisión de Markov (MDP) y lo resuelve usando
    el algoritmo de Iteración de Políticas. Este método alterna entre
    evaluar una política y mejorarla hasta que converge a la óptima.
    """

    def __init__(self, estados, acciones, transiciones, recompensas, gamma=0.9, theta=1e-4):
        self.estados = estados
        self.acciones = acciones
        self.transiciones = transiciones
        self.recompensas = recompensas
        self.gamma = gamma  # Factor de descuento
        self.theta = theta  # Umbral para la convergencia de la evaluación

        # 1. Inicialización
        # Se inicia con una función de valor V(s) = 0 para todos los estados.
        self.V = {s: 0.0 for s in self.estados}
        # Se inicia con una política completamente aleatoria.
        self.politica = {s: np.random.choice(self.acciones) for s in self.estados}
        self.politica['S3'] = 'TERMINAL' # El estado final no tiene acciones.

    def solve(self):
        """
        Ejecuta el bucle principal de Iteración de Políticas hasta que la política se estabiliza.
        """
        iteracion = 0
        while True:
            iteracion += 1
            print(f"\n--- Iteración Global {iteracion} ---")
            
            # --- FASE 1: Evaluación de la Política ---
            # Se calcula el valor V(s) para la política actual.
            self._evaluar_politica_actual()
            print(f"  Política Evaluada: {self.politica}")
            print(f"  Valores V(s) resultantes: {{'S0': {self.V['S0']:.3f}, 'S1': {self.V['S1']:.3f}, ...}}")

            # --- FASE 2: Mejora de la Política ---
            # Se actualiza la política basándose en los nuevos valores de V(s).
            politica_es_estable = self._mejorar_politica()
            
            # Si la política no cambió en esta iteración, hemos encontrado la óptima.
            if politica_es_estable:
                print("\nConvergencia alcanzada: la política se ha estabilizado.")
                break
        
        return self.politica, self.V

    def _evaluar_politica_actual(self):
        """
        Calcula V(s) para la política actual hasta la convergencia.
        (Iterative Policy Evaluation)
        """
        while True:
            delta = 0
            for s in self.estados:
                if s == 'S3': continue # El valor del estado terminal es su recompensa.
                
                v_antiguo = self.V[s]
                accion_fijada = self.politica[s]
                estado_siguiente = self.transiciones[s][accion_fijada]
                
                # Ecuación de Bellman para una política fija: V(s) = R(s) + γ * V(s')
                self.V[s] = self.recompensas[s] + self.gamma * self.V[estado_siguiente]
                
                delta = max(delta, abs(v_antiguo - self.V[s]))
                
            if delta < self.theta:
                break

    def _mejorar_politica(self):
        """
        Actualiza la política eligiendo la acción que maximiza la utilidad esperada
        (acción "greedy") según la función de valor actual V(s).
        """
        politica_estable = True
        for s in self.estados:
            if s == 'S3': continue

            accion_antigua = self.politica[s]
            
            # Calcular el valor Q(s,a) para cada acción posible.
            valores_q = {}
            for a in self.acciones:
                estado_siguiente = self.transiciones[s][a]
                valores_q[a] = self.recompensas[s] + self.gamma * self.V[estado_siguiente]
            
            # Encontrar la mejor acción.
            mejor_accion = max(valores_q, key=valores_q.get)
            
            # Actualizar la política.
            self.politica[s] = mejor_accion
            
            # Comprobar si la política ha cambiado.
            if accion_antigua != mejor_accion:
                politica_estable = False
        
        return politica_estable

# --- 1. DEFINICIÓN DEL PROBLEMA ---
ESTADOS_MDP = ['S0', 'S1', 'S2', 'S3']
ACCIONES_MDP = ['N', 'S', 'E', 'O']
TRANSICIONES_MDP = {
    'S0': {'N': 'S2', 'E': 'S1', 'S': 'S0', 'O': 'S0'},
    'S1': {'N': 'S3', 'O': 'S0', 'S': 'S1', 'E': 'S1'},
    'S2': {'E': 'S3', 'S': 'S0', 'N': 'S2', 'O': 'S2'},
    'S3': {'N': 'S3', 'S': 'S3', 'E': 'S3', 'O': 'S3'}
}
RECOMPENSAS_MDP = {'S0': 0, 'S1': 0, 'S2': 0, 'S3': 10}

# --- 2. EJECUCIÓN ---
solucionador = PolicyIterationSolver(
    estados=ESTADOS_MDP,
    acciones=ACCIONES_MDP,
    transiciones=TRANSICIONES_MDP,
    recompensas=RECOMPENSAS_MDP,
    gamma=0.9 # Factor de descuento alto para valorar el futuro
)
politica_optima, valores_optimos = solucionador.solve()

# --- 3. RESULTADOS ---
print("\n" + "="*50)
print("Resultado Final:")
print("\nPolítica Óptima π*(s):")
for estado, accion in politica_optima.items():
    print(f"  En {estado}, la mejor acción es: {accion}")

print("\nFunción de Valor Óptima V*(s):")
for estado, valor in valores_optimos.items():
    print(f"  El valor de {estado} es: {valor:.3f}")