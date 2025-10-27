# =========================================================================
# Agente de Búsqueda Online con Aprendizaje (Implementación OOP de LRTA*)
# =========================================================================

import math

class AgenteLRTA:
    """
    Representa a un agente que navega por un entorno desconocido utilizando LRTA*.
    El agente toma decisiones basadas en su conocimiento actual (heurísticas) y
    actualiza ese conocimiento a medida que explora.
    """

    def __init__(self, posicion_inicial, heuristica_inicial):
        """
        Inicializa al agente con su punto de partida y su mapa mental inicial.
        """
        self.posicion_actual = posicion_inicial
        self.conocimiento_h = heuristica_inicial  # El "mapa mental" del agente.
        print(f"🤖 Agente creado en '{self.posicion_actual}'. Conocimiento inicial: {self.conocimiento_h}")

    def decidir_proximo_movimiento(self, entorno):
        """
        El núcleo de la decisión de LRTA*:
        1. Evalúa las opciones desde su posición actual.
        2. Actualiza su conocimiento sobre su posición actual (aprende).
        3. Elige el mejor movimiento.
        """
        # Opciones de movimiento desde la posición actual del agente.
        opciones = entorno.get(self.posicion_actual, {})
        if not opciones:
            return None, None # No hay a dónde ir.

        mejor_opcion_costo_f = float('inf')
        mejor_sucesor = None
        costo_del_movimiento = None

        # 1. Evaluar todas las opciones posibles (sucesores).
        for sucesor, costo_real_tramo in opciones.items():
            # Costo estimado f(S') = costo_real(S, S') + h(S')
            # El agente combina el costo real de moverse con su estimación del costo restante.
            costo_f_estimado = costo_real_tramo + self.conocimiento_h.get(sucesor, float('inf'))
            
            if costo_f_estimado < mejor_opcion_costo_f:
                mejor_opcion_costo_f = costo_f_estimado
                mejor_sucesor = sucesor
                costo_del_movimiento = costo_real_tramo

        # 2. Aprender: Actualizar el "mapa mental" del agente sobre su posición actual.
        # h(S) <- min[ costo_real(S, S') + h(S') ]
        print(f"  🧠 Aprendizaje en '{self.posicion_actual}': h({self.posicion_actual}) cambia de {self.conocimiento_h[self.posicion_actual]} a {mejor_opcion_costo_f}.")
        self.conocimiento_h[self.posicion_actual] = mejor_opcion_costo_f
        
        return mejor_sucesor, costo_del_movimiento

    def moverse(self, nueva_posicion):
        """Actualiza la posición del agente."""
        print(f"  ➡️  Agente se mueve a '{nueva_posicion}'.")
        self.posicion_actual = nueva_posicion

# --- 1. CONFIGURACIÓN DEL ENTORNO Y EL AGENTE ---
# El mapa del mundo real con los costos de cada tramo.
ENTORNO_REAL = {
    'A': {'B': 1},
    'B': {'A': 1, 'C': 2},
    'C': {}  # Meta
}

# El conocimiento inicial (y posiblemente incorrecto) que tiene el agente.
HEURISTICA_INICIAL = {'A': 3, 'B': 1, 'C': 0}

INICIO = 'A'
META = 'C'

# --- 2. SIMULACIÓN DE LA BÚSQUEDA ---
agente = AgenteLRTA(INICIO, HEURISTICA_INICIAL)
ruta_recorrida = [INICIO]
costo_total_real = 0

print("-" * 50)

while agente.posicion_actual != META:
    # 1. El agente piensa y decide su próximo movimiento, aprendiendo en el proceso.
    siguiente_destino, costo_movimiento = agente.decidir_proximo_movimiento(ENTORNO_REAL)
    
    if siguiente_destino is None:
        print("Búsqueda fallida: el agente está en un punto sin salida.")
        break
    
    # 2. El agente se mueve físicamente al nuevo destino.
    agente.moverse(siguiente_destino)
    
    # 3. Se registra el progreso.
    ruta_recorrida.append(siguiente_destino)
    costo_total_real += costo_movimiento
    print(f"    Conocimiento actual del agente: {agente.conocimiento_h}")
    print("-" * 50)

# --- 3. RESULTADOS FINALES ---
if agente.posicion_actual == META:
    print(f"🏁 ¡META ALCANZADA: '{META}'!")
    print(f"  Ruta final: {' → '.join(ruta_recorrida)}")
    print(f"  Costo real del viaje: {costo_total_real}")