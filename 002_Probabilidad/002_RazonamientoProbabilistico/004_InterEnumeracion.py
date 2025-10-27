# =========================================================================
# Inferencia por Enumeración en Redes Bayesianas (Versión OOP y Recursiva)
# =========================================================================

class MotorDeInferencia:
    """
    Representa una Red Bayesiana y puede realizar inferencia por enumeración
    de forma general para cualquier consulta.
    """

    def __init__(self, estructura_red):
        """
        Inicializa el motor con la topología y las CPTs de la red.
        """
        self.nodos = estructura_red['nodos'] # Nodos en orden topológico
        self.padres = estructura_red['padres']
        self.cpts = estructura_red['cpts']

    def _obtener_probabilidad(self, variable, valor, evidencia):
        """
        Obtiene la probabilidad P(Variable=valor | Padres(Variable)) desde la CPT.
        """
        padres_de_var = self.padres[variable]
        if not padres_de_var:
            # Es un nodo raíz, no tiene padres.
            return self.cpts[variable][valor]
        else:
            # Es un nodo con padres, se necesita la configuración de los padres.
            configuracion_padres = tuple(evidencia[p] for p in padres_de_var)
            return self.cpts[variable][configuracion_padres][valor]

    def _enumerar_todo(self, variables, evidencia):
        """
        Función recursiva que suma las probabilidades de todas las posibles
        asignaciones de las variables ocultas.
        """
        # Caso Base: Si no quedan más variables, la probabilidad es 1.
        if not variables:
            return 1.0
        
        primera, resto = variables[0], variables[1:]
        
        if primera in evidencia:
            # Caso 1: La variable ya tiene un valor asignado en la evidencia.
            prob = self._obtener_probabilidad(primera, evidencia[primera], evidencia)
            return prob * self._enumerar_todo(resto, evidencia)
        else:
            # Caso 2: Es una variable oculta, por lo que se debe sumar (marginalizar).
            suma_ponderada = 0
            for valor in self.cpts[primera]['valores']:
                evidencia_extendida = evidencia.copy()
                evidencia_extendida[primera] = valor
                prob = self._obtener_probabilidad(primera, valor, evidencia_extendida)
                suma_ponderada += prob * self._enumerar_todo(resto, evidencia_extendida)
            return suma_ponderada

    def consultar(self, var_consulta, evidencia):
        """
        Calcula la distribución de probabilidad P(Consulta | Evidencia).
        """
        distribucion_q = {}
        
        # Para cada posible valor de la variable de consulta...
        for valor_consulta in self.cpts[var_consulta]['valores']:
            # ...se calcula su probabilidad no normalizada.
            evidencia_extendida = evidencia.copy()
            evidencia_extendida[var_consulta] = valor_consulta
            distribucion_q[valor_consulta] = self._enumerar_todo(self.nodos, evidencia_extendida)
        
        # Normalizar el resultado para que sume 1.
        total = sum(distribucion_q.values())
        return {valor: prob / total for valor, prob in distribucion_q.items()}

# --- 1. DEFINICIÓN DE LA ESTRUCTURA DE LA RED ---
ESTRUCTURA_ALARMA = {
    'nodos': ['Robo', 'Alarma', 'JuanLlama'], # Nodos en orden topológico
    'padres': {
        'Robo': [],
        'Alarma': ['Robo'],
        'JuanLlama': ['Alarma']
    },
    'cpts': {
        'Robo':      {'valores': ['Si', 'No'], 'Si': 0.001, 'No': 0.999},
        'Alarma':    {'valores': ['Si', 'No'], ('Si',): {'Si': 0.95, 'No': 0.05}, ('No',): {'Si': 0.01, 'No': 0.99}},
        'JuanLlama': {'valores': ['Si', 'No'], ('Si',): {'Si': 0.90, 'No': 0.10}, ('No',): {'Si': 0.05, 'No': 0.95}}
    }
}

# --- 2. EJECUCIÓN DE LA INFERENCIA ---
# Se crea una instancia del motor con la estructura de la red.
motor_inferencia = MotorDeInferencia(ESTRUCTURA_ALARMA)

# Se define la consulta: P(Robo | JuanLlama='Si')
VARIABLE_CONSULTA = 'Robo'
EVIDENCIA = {'JuanLlama': 'Si'}

# Se realiza la inferencia.
resultado = motor_inferencia.consultar(VARIABLE_CONSULTA, EVIDENCIA)

# --- 3. RESULTADOS ---
print(f"--- Inferencia por Enumeración: P({VARIABLE_CONSULTA} | {EVIDENCIA}) ---")
print("\nResultado Final:")
for valor, probabilidad in resultado.items():
    print(f"  P({VARIABLE_CONSULTA}={valor} | {list(EVIDENCIA.keys())[0]}={list(EVIDENCIA.values())[0]}) = {probabilidad:.4f}")