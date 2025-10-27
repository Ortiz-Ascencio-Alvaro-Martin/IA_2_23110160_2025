# = =======================================================================
# Q-Learning para el Problema del Acantilado (Versión Orientada a Objetos)
# Objetivo: Encontrar la ruta más segura y eficiente desde el inicio a la meta.
# =========================================================================

import random
import numpy as np

class EntornoAcantilado:
    """
    Representa el mundo del "acantilado". Conoce las reglas del entorno,
    como las dimensiones, la ubicación del acantilado y las recompensas.
    """
    def __init__(self, filas, cols, inicio):
        self.filas = filas
        self.cols = cols
        self.inicio = inicio
        self.meta = (0, cols - 1)
        self.acantilado = [(0, c) for c in range(1, cols - 1)]

    def obtener_transicion(self, estado, accion):
        """
        Calcula el estado siguiente y la recompensa, dadas una acción y un estado.
        """
        r, c = estado
        
        # Movimiento base
        if accion == 'N':   r += 1
        elif accion == 'S': r -= 1
        elif accion == 'E': c += 1
        elif accion == 'O': c -= 1
        
        # Comprobar si se sale de los límites
        r = max(0, min(r, self.filas - 1))
        c = max(0, min(c, self.cols - 1))
        
        estado_siguiente = (r, c)
        recompensa = -1 # Costo por cada paso

        # Comprobar si cae al acantilado
        if estado_siguiente in self.acantilado:
            recompensa = -100
            estado_siguiente = self.inicio # Regresa al inicio
            
        return estado_siguiente, recompensa

class AgenteQLearning:
    """
    Representa al agente que aprende. Mantiene la Q-Table y decide qué
    acciones tomar usando una política epsilon-greedy.
    """
    def __init__(self, acciones, alpha, gamma, epsilon):
        self.acciones = acciones
        self.alpha = alpha     # Tasa de aprendizaje
        self.gamma = gamma     # Factor de descuento
        self.epsilon = epsilon # Tasa de exploración
        # La Q-Table se inicializa vacía y se llena bajo demanda.
        self.q_tabla = {}

    def _obtener_q_valor(self, estado, accion):
        """Devuelve el valor Q para un par (estado, acción), inicializándolo si no existe."""
        return self.q_tabla.setdefault(estado, {a: 0.0 for a in self.acciones})[accion]

    def elegir_accion(self, estado):
        """
        Elige una acción usando una política epsilon-greedy: explora con
        probabilidad epsilon, de lo contrario, explota el mejor conocimiento actual.
        """
        if random.random() < self.epsilon:
            return random.choice(self.acciones) # Exploración
        else:
            q_valores = self.q_tabla.get(estado, {a: 0.0 for a in self.acciones})
            return max(q_valores, key=q_valores.get) # Explotación

    def aprender(self, estado, accion, recompensa, estado_siguiente, estado_meta):
        """
        Actualiza la Q-Table usando la regla de actualización de Q-Learning.
        """
        # --- Actualización Q-Learning ---
        # Q(s,a) <- Q(s,a) + α * [ R + γ * max_a' Q(s',a') - Q(s,a) ]
        
        valor_q_actual = self._obtener_q_valor(estado, accion)
        
        # El valor del estado meta siempre es 0, no hay futuro.
        if estado_siguiente == estado_meta:
            valor_max_futuro = 0.0
        else:
            q_valores_siguientes = self.q_tabla.get(estado_siguiente, {a: 0.0 for a in self.acciones})
            valor_max_futuro = max(q_valores_siguientes.values())
            
        # Objetivo de la Diferencia Temporal (TD Target)
        objetivo_td = recompensa + self.gamma * valor_max_futuro
        
        # Actualizar el valor Q
        nuevo_valor_q = valor_q_actual + self.alpha * (objetivo_td - valor_q_actual)
        self.q_tabla[estado][accion] = nuevo_valor_q

# --- 1. CONFIGURACIÓN E INICIALIZACIÓN ---
entorno = EntornoAcantilado(filas=4, cols=12, inicio=(0, 0))
agente = AgenteQLearning(acciones=['N', 'S', 'E', 'O'], alpha=0.1, gamma=0.9, epsilon=0.1)
EPISODIOS = 500

# --- 2. BUCLE PRINCIPAL DE APRENDIZAJE ---
for episodio in range(EPISODIOS):
    estado = entorno.inicio
    while estado != entorno.meta:
        # 1. El agente elige una acción.
        accion = agente.elegir_accion(estado)
        # 2. El entorno responde con un nuevo estado y una recompensa.
        estado_siguiente, recompensa = entorno.obtener_transicion(estado, accion)
        # 3. El agente aprende de esta experiencia.
        agente.aprender(estado, accion, recompensa, estado_siguiente, entorno.meta)
        # 4. Se actualiza el estado.
        estado = estado_siguiente

# --- 3. EXTRACCIÓN Y VISUALIZACIÓN DE LA POLÍTICA ---
politica = {}
for r in range(entorno.filas):
    for c in range(entorno.cols):
        estado = (r, c)
        if estado not in entorno.acantilado and estado != entorno.meta:
            politica[estado] = agente.elegir_accion(estado) # Usar epsilon=0 para la política final

# Crear una visualización del camino
grid = [['·' for _ in range(entorno.cols)] for _ in range(entorno.filas)]
for r, c in entorno.acantilado: grid[r][c] = 'C'
grid[entorno.inicio[0]][entorno.inicio[1]] = 'S'
grid[entorno.meta[0]][entorno.meta[1]] = 'G'

# Dibujar el camino óptimo
estado_actual = entorno.inicio
path = []
while estado_actual != entorno.meta and estado_actual not in path:
    path.append(estado_actual)
    accion_optima = max(agente.q_tabla.get(estado_actual, {}), key=agente.q_tabla.get(estado_actual, {}).get)
    r, c = estado_actual
    if (r,c) != entorno.inicio:
        grid[r][c] = {'N': '^', 'S': 'v', 'E': '>', 'O': '<'}.get(accion_optima, '*')
    estado_actual, _ = entorno.obtener_transicion(estado_actual, accion_optima)
    if len(path) > 50: break # Límite de seguridad

print("--- Política Óptima Encontrada por Q-Learning ---")
# Imprimir el grid de abajo hacia arriba para que (0,0) esté en la esquina inferior izquierda.
for fila in reversed(grid):
    print(" ".join(fila))