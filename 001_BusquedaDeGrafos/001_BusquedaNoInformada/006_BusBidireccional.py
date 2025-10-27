# =================================================================
# Búsqueda de Encuentro en el Medio (OOP Bidirectional Search)
# =================================================================

from collections import deque

class BuscadorBidireccional:
    """
    Encapsula la lógica para una búsqueda bidireccional en un grafo.
    Inicia dos búsquedas BFS simultáneamente: una desde el origen y otra
    desde el destino, esperando a que se encuentren en un punto intermedio.
    """

    def __init__(self, red, punto_inicio, punto_final):
        """
        Prepara la búsqueda inicializando todos los componentes necesarios.
        """
        self.red_directa = red
        self.red_inversa = self._invertir_red(red) # Necesaria para la búsqueda hacia atrás.
        self.inicio = punto_inicio
        self.meta = punto_final

        # 1. Se crea una estructura para gestionar el estado de ambas búsquedas.
        #    'delantera': avanza desde el inicio.
        #    'trasera': retrocede desde la meta.
        self.frentes = {
            'delantera': self._crear_frente(punto_inicio),
            'trasera': self._crear_frente(punto_final)
        }

    def _crear_frente(self, nodo_inicial):
        """Función auxiliar para inicializar la estructura de un frente de búsqueda."""
        return {
            'cola': deque([nodo_inicial]),
            'visitados': {nodo_inicial},
            'padres': {nodo_inicial: None}
        }

    def _invertir_red(self, red_original):
        """
        Crea un grafo con todas las conexiones (aristas) en dirección opuesta.
        Si A -> B en la original, entonces B -> A en la inversa.
        """
        red_invertida = {nodo: [] for nodo in red_original}
        for nodo, conexiones in red_original.items():
            for conexion in conexiones:
                if conexion not in red_invertida:
                    red_invertida[conexion] = []
                red_invertida[conexion].append(nodo)
        return red_invertida

    def buscar(self):
        """
        Ejecuta el algoritmo de búsqueda principal, alternando entre los frentes.
        """
        if self.inicio == self.meta:
            return f"El punto de partida y la meta son el mismo: {self.inicio}."

        # 2. El bucle se ejecuta mientras ambos frentes tengan nodos por explorar.
        while self.frentes['delantera']['cola'] and self.frentes['trasera']['cola']:
            
            # 3. Avanza un paso el frente que parte del INICIO.
            punto_encuentro = self._expandir_un_frente('delantera', 'trasera', self.red_directa)
            if punto_encuentro:
                print(f"Ambas búsquedas se encontraron en el nodo: '{punto_encuentro}'")
                return self._ensamblar_ruta_completa(punto_encuentro)

            # 4. Avanza un paso el frente que parte de la META (hacia atrás).
            punto_encuentro = self._expandir_un_frente('trasera', 'delantera', self.red_inversa)
            if punto_encuentro:
                print(f"Ambas búsquedas se encontraron en el nodo: '{punto_encuentro}'")
                return self._ensamblar_ruta_completa(punto_encuentro)
        
        return "Búsqueda fallida. No existe un camino entre los puntos."

    def _expandir_un_frente(self, frente_actual_key, frente_opuesto_key, red_a_usar):
        """
        Procesa un nivel de la búsqueda BFS para un frente dado.
        Retorna el nodo de intersección si lo encuentra.
        """
        frente_actual = self.frentes[frente_actual_key]
        frente_opuesto = self.frentes[frente_opuesto_key]
        
        nodo_a_explorar = frente_actual['cola'].popleft()

        # 5. La condición clave: ¿El nodo que estoy explorando ya fue visitado por la OTRA búsqueda?
        if nodo_a_explorar in frente_opuesto['visitados']:
            return nodo_a_explorar # ¡Encuentro!

        # 6. Si no hay encuentro, expande a los vecinos.
        for vecino in red_a_usar.get(nodo_a_explorar, []):
            if vecino not in frente_actual['visitados']:
                frente_actual['visitados'].add(vecino)
                frente_actual['padres'][vecino] = nodo_a_explorar
                frente_actual['cola'].append(vecino)
        
        return None # No se encontró un punto de encuentro en este paso.

    def _ensamblar_ruta_completa(self, punto_encuentro):
        """
        Una vez encontrado el punto de encuentro, reconstruye el camino completo
        trazando la ruta desde ambos lados hasta dicho punto.
        """
        # Trazar ruta desde el INICIO hasta el punto de encuentro
        ruta_delantera = []
        nodo_actual = punto_encuentro
        while nodo_actual is not None:
            ruta_delantera.append(nodo_actual)
            nodo_actual = self.frentes['delantera']['padres'].get(nodo_actual)
        
        # Trazar ruta desde la META hasta el punto de encuentro
        ruta_trasera = []
        nodo_actual = self.frentes['trasera']['padres'].get(punto_encuentro) # Excluimos el punto de encuentro
        while nodo_actual is not None:
            ruta_trasera.append(nodo_actual)
            nodo_actual = self.frentes['trasera']['padres'].get(nodo_actual)

        # La ruta final es la primera parte (en orden) + la segunda parte (invertida)
        ruta_final = list(reversed(ruta_delantera)) + ruta_trasera
        return f"Ruta óptima encontrada: {' → '.join(ruta_final)}"

# --- Ejemplo de Uso ---
mapa = {
    'A': ['B', 'G'], 'B': ['C', 'H'], 'C': ['D'], 'D': ['E'], 'E': ['F'],
    'F': ['I'], 'G': ['J'], 'H': ['K', 'L'], 'I': [], 'J': [], 'K': ['M'],
    'L': ['M'], 'M': [] # Objetivo
}
INICIO = 'A'
OBJETIVO = 'M'

print(f"Grafo (Mapa): {mapa}")
print("-" * 50)

# 1. Se crea una instancia del buscador.
buscador = BuscadorBidireccional(mapa, INICIO, OBJETIVO)
# 2. Se ejecuta la búsqueda.
resultado = buscador.buscar()

print(f"Resultado de la Búsqueda ({INICIO} → {OBJETIVO}):")
print(resultado)