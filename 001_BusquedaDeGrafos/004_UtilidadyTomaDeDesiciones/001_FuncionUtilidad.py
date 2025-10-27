# =========================================================================
# Análisis de Decisiones de Inversión Basado en Utilidad Esperada (MEU)
# Implementación Orientada a Objetos
# =========================================================================

class OpcionDeInversion:
    """
    Representa una posible decisión de inversión. Contiene los posibles
    resultados y puede calcular su propia utilidad esperada.
    """

    def __init__(self, nombre, posibles_resultados):
        """
        Inicializa la opción de inversión.
        - nombre: Un identificador para la opción (ej. "Bonos del Gobierno").
        - posibles_resultados: Un diccionario donde la clave es el nombre del
          resultado y el valor es una tupla (probabilidad, utilidad).
        """
        self.nombre = nombre
        self.resultados = posibles_resultados
        self.utilidad_esperada = self._calcular_eu()

    def _calcular_eu(self):
        """
        Calcula la Utilidad Esperada (EU) para esta opción de inversión.
        La fórmula es: EU = Σ [Probabilidad(resultado) * Utilidad(resultado)]
        """
        eu_total = 0
        for _, (probabilidad, utilidad) in self.resultados.items():
            eu_total += probabilidad * utilidad
        return eu_total

# --- 1. Definición de las Opciones de Inversión ---

# Opción 1: Una inversión conservadora con resultados modestos.
inversion_segura = OpcionDeInversion(
    nombre="Bonos del Gobierno (Bajo Riesgo)",
    posibles_resultados={
        'Ganancia Alta': (0.3, 50),
        'Ganancia Media': (0.6, 20),
        'Sin Ganancia': (0.1, 0)
    }
)

# Opción 2: Una inversión de alto riesgo con potencial de alta recompensa o pérdida.
inversion_arriesgada = OpcionDeInversion(
    nombre="Startup Tecnológica (Alto Riesgo)",
    posibles_resultados={
        'Éxito Masivo': (0.1, 100),
        'Fracaso Total': (0.9, -5)
    }
)

# --- 2. Análisis y Decisión ---

# Se agrupan todas las opciones para analizarlas.
opciones = [inversion_segura, inversion_arriesgada]

print("--- Análisis de Utilidad para Decisiones de Inversión ---")
for opcion in opciones:
    print(f"  - Opción: '{opcion.nombre}'")
    print(f"    Utilidad Esperada (EU): {opcion.utilidad_esperada:.2f}")

# Se utiliza la función max() para encontrar la opción con la mayor utilidad esperada.
# La clave de la comparación es el atributo 'utilidad_esperada' de cada objeto.
mejor_decision = max(opciones, key=lambda opcion: opcion.utilidad_esperada)

print("\n--- Decisión del Agente Racional (Principio de MEU) ---")
print(f"La estrategia óptima es elegir: '{mejor_decision.nombre}'")
print(f"Utilidad Máxima Esperada (MEU): {mejor_decision.utilidad_esperada:.2f}")