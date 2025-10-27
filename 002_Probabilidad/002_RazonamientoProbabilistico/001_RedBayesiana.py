# =========================================================================
# Motor de Inferencia para Redes Bayesianas (Versión Orientada a Objetos)
# Problema: Inferencia en la red de Alarma de Robo.
# =========================================================================

import itertools

class MotorRedBayesiana:
    """
    Representa una Red Bayesiana y puede realizar inferencia por enumeración.
    """

    def __init__(self, estructura_red):
        """
        Inicializa el motor con la topología y las Tablas de Probabilidad
        Condicional (CPT) de la red.
        """
        self.nodos = estructura_red['nodos']
        self.padres = estructura_red['padres']
        self.cpts = estructura_red['cpts']

    def _obtener_probabilidad(self, variable, valor, evidencia):
        """
        Obtiene la probabilidad P(Variable=valor | Padres(Variable)) desde la CPT.
        """
        padres_de_var = self.padres[variable]
        if not padres_de_var:
            # Nodo raíz, no tiene padres.
            return self.cpts[variable][valor]
        else:
            # Nodo con padres, se necesita la configuración de los padres.
            configuracion_padres = tuple(evidencia[p] for p in padres_de_var)
            return self.cpts[variable][configuracion_padres][valor]

    def inferencia_por_enumeracion(self, var_consulta, evidencia):
        """
        Calcula la distribución de probabilidad condicional P(Consulta | Evidencia)
        usando el algoritmo de enumeración.
        """
        distribucion_q = {}
        
        # Itera sobre cada posible valor de la variable de consulta.
        for valor_consulta in self.cpts[var_consulta]['valores']:
            
            # Extender la evidencia con el valor actual de la variable de consulta.
            evidencia_extendida = evidencia.copy()
            evidencia_extendida[var_consulta] = valor_consulta
            
            # Sumar sobre todas las variables ocultas.
            distribucion_q[valor_consulta] = self._enumerar_todas(self.nodos, evidencia_extendida)
        
        # Normalizar el resultado para que sume 1.
        total = sum(distribucion_q.values())
        for valor, prob in distribucion_q.items():
            distribucion_q[valor] = prob / total
            
        return distribucion_q

    def _enumerar_todas(self, variables, evidencia):
        """
        Función recursiva que suma las probabilidades de todas las posibles
        asignaciones de las variables ocultas.
        """
        if not variables:
            return 1.0
        
        primera, resto = variables[0], variables[1:]
        
        if primera in evidencia:
            # Si la variable ya tiene un valor en la evidencia, se usa ese.
            prob = self._obtener_probabilidad(primera, evidencia[primera], evidencia)
            return prob * self._enumerar_todas(resto, evidencia)
        else:
            # Si es una variable oculta, se suma sobre todos sus posibles valores.
            suma = 0
            for valor in self.cpts[primera]['valores']:
                evidencia_extendida = evidencia.copy()
                evidencia_extendida[primera] = valor
                prob = self._obtener_probabilidad(primera, valor, evidencia_extendida)
                suma += prob * self._enumerar_todas(resto, evidencia_extendida)
            return suma

# --- 1. DEFINICIÓN DE LA ESTRUCTURA DE LA RED ---
ESTRUCTURA_ALARMA = {
    'nodos': ['Robo', 'Alarma', 'JuanLlama'], # Orden topológico
    'padres': {
        'Robo': [],
        'Alarma': ['Robo'],
        'JuanLlama': ['Alarma']
    },
    'cpts': {
        'Robo': {'valores': ['Si', 'No'], 'Si': 0.001, 'No': 0.999},
        'Alarma': {
            'valores': ['Si', 'No'],
            ('Si',): {'Si': 0.95, 'No': 0.05}, # P(Alarma | Robo=Si)
            ('No',): {'Si': 0.01, 'No': 0.99}  # P(Alarma | Robo=No)
        },
        'JuanLlama': {
            'valores': ['Si', 'No'],
            ('Si',): {'Si': 0.90, 'No': 0.10}, # P(JuanLlama | Alarma=Si)
            ('No',): {'Si': 0.05, 'No': 0.95}  # P(JuanLlama | Alarma=No)
        }
    }
}

# --- 2. EJECUCIÓN DE LA INFERENCIA ---
# Se crea una instancia del motor de inferencia con la estructura de la red.
motor_bn = MotorRedBayesiana(ESTRUCTURA_ALARMA)

# Se define la consulta y la evidencia.
VARIABLE_CONSULTA = 'Robo'
EVIDENCIA = {'JuanLlama': 'Si'}

# Se realiza la inferencia.
resultado_inferencia = motor_bn.inferencia_por_enumeracion(VARIABLE_CONSULTA, EVIDENCIA)

# --- 3. RESULTADOS ---
print("--- Inferencia en Red Bayesiana con Enumeración ---")
print(f"Consulta: P({VARIABLE_CONSULTA} | {EVIDENCIA})")
print("\nResultado de la Inferencia:")
for valor, probabilidad in resultado_inferencia.items():
    print(f"  P({VARIABLE_CONSULTA}={valor} | {EVIDENCIA}) = {probabilidad:.4f}")