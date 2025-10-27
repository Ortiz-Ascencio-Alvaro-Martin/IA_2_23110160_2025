# =========================================================================
# Solucionador de Juegos para Encontrar el Equilibrio de Nash (Versión OOP)
# Problema: El Dilema del Prisionero
# =========================================================================

import numpy as np
import itertools

class GameSolver:
    """
    Encapsula la lógica para un juego de 2 jugadores y 2 acciones,
    y encuentra el Equilibrio de Nash en estrategias puras.
    """

    def __init__(self, players, actions, payoff_matrix):
        """
        Inicializa el juego con sus componentes.
        - payoff_matrix: Una matriz donde payoff_matrix[a1][a2] = (utilidad_p1, utilidad_p2).
        """
        self.players = players
        self.actions = actions
        self.payoffs = payoff_matrix
        # Mapeo de acciones a índices para un fácil acceso a la matriz.
        self.action_map = {action: i for i, action in enumerate(actions)}

    def _get_best_response(self, player_id, opponent_action):
        """
        Encuentra la mejor acción para un jugador, dada la acción de su oponente.
        """
        opponent_action_idx = self.action_map[opponent_action]
        best_utility = -np.inf
        best_action = None

        # Itera sobre todas las acciones posibles para el jugador actual.
        for action in self.actions:
            action_idx = self.action_map[action]
            
            if player_id == 0: # Jugador 1
                # La utilidad está en PAYOFFS[acción_p1][acción_p2][0]
                utility = self.payoffs[action_idx][opponent_action_idx][0]
            else: # Jugador 2
                # La utilidad está en PAYOFFS[acción_p1][acción_p2][1]
                utility = self.payoffs[opponent_action_idx][action_idx][1]

            if utility > best_utility:
                best_utility = utility
                best_action = action
        
        return best_action

    def find_nash_equilibrium(self):
        """
        Itera sobre todos los perfiles de estrategia para encontrar aquellos
        donde ningún jugador tiene un incentivo para cambiar su acción unilateralmente.
        """
        equilibria = []
        
        # Genera todas las combinaciones de estrategias posibles (ej. (C, C), (C, NC), etc.).
        all_strategy_profiles = list(itertools.product(self.actions, repeat=len(self.players)))
        
        for profile in all_strategy_profiles:
            p1_action, p2_action = profile
            
            # 1. Comprobar si la acción del Jugador 1 es la mejor respuesta a la del Jugador 2.
            p1_best_response = self._get_best_response(player_id=0, opponent_action=p2_action)
            is_p1_stable = (p1_action == p1_best_response)
            
            # 2. Comprobar si la acción del Jugador 2 es la mejor respuesta a la del Jugador 1.
            p2_best_response = self._get_best_response(player_id=1, opponent_action=p1_action)
            is_p2_stable = (p2_action == p2_best_response)
            
            # 3. Si ambas son mejores respuestas mutuas, es un Equilibrio de Nash.
            if is_p1_stable and is_p2_stable:
                p1_payoff, p2_payoff = self.payoffs[self.action_map[p1_action]][self.action_map[p2_action]]
                equilibria.append({
                    'profile': profile,
                    'payoffs': (p1_payoff, p2_payoff)
                })
                
        return equilibria

# --- 1. DEFINICIÓN DEL JUEGO: DILEMA DEL PRISIONERO ---
PLAYERS = ['P1', 'P2']
ACTIONS = ['Confesar', 'No Confesar']

# La matriz de pagos se define como una lista de listas (o un array de NumPy).
# Filas: Acciones de P1, Columnas: Acciones de P2
# Formato: (Utilidad P1, Utilidad P2)
PAYOFF_MATRIX = [
    # P2: Confesar      | P2: No Confesar
    [(-5, -5),           (0, -10)],      # Fila para P1: Confesar
    [(-10, 0),           (-1, -1)]       # Fila para P1: No Confesar
]

# --- 2. EJECUCIÓN ---
# Se crea una instancia del solucionador con la definición del juego.
prisoner_dilemma = GameSolver(PLAYERS, ACTIONS, PAYOFF_MATRIX)

# Se busca el equilibrio.
nash_equilibria = prisoner_dilemma.find_nash_equilibrium()

# --- 3. RESULTADOS ---
print("--- Búsqueda de Equilibrio de Nash en el Dilema del Prisionero ---")
if nash_equilibria:
    print("\n¡Equilibrio(s) de Nash encontrado(s)!")
    for eq in nash_equilibria:
        p1_act, p2_act = eq['profile']
        p1_pay, p2_pay = eq['payoffs']
        print(f"  - Perfil de Estrategia: (P1: {p1_act}, P2: {p2_act})")
        print(f"  - Pagos Resultantes: (P1: {p1_pay}, P2: {p2_pay})")
        print("    Análisis: Racionalmente, ambos jugadores confiesan, llevando a un resultado peor para ambos que si hubieran cooperado.")
else:
    print("\nNo se encontró un Equilibrio de Nash en estrategias puras.")