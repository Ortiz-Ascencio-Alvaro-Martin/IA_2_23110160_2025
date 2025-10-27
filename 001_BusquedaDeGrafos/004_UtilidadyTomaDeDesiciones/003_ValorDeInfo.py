# =========================================================================
# Valor de la Información (VOI) - Implementación Orientada a Objetos
# Problema: Decidir si invertir basándose en un informe económico.
# =========================================================================

class AnalizadorVOI:
    """
    Encapsula un problema de decisión para calcular el Valor de la Información.
    Compara la mejor decisión que se puede tomar sin información adicional
    contra la utilidad esperada de tomar decisiones después de recibirla.
    """

    def __init__(self, problema):
        """Inicializa el analizador con la definición completa del problema."""
        self.acciones = problema['utilidades']
        self.p_inicial = problema['probabilidades_iniciales']
        self.p_evidencia = problema['probabilidades_evidencia']
        self.p_condicional = problema['probabilidades_condicionales']
        self.nombres_acciones = list(self.acciones.keys())

    def _calcular_eu(self, accion, probabilidades_estado):
        """Calcula la Utilidad Esperada (EU) para una acción dada."""
        return sum(
            prob * self.acciones[accion][estado]
            for estado, prob in probabilidades_estado.items()
        )

    def calcular_voi(self):
        """
        Orquesta el cálculo completo del VOI.
        VOI = EU(con información) - MEU(sin información)
        """
        # --- 1. Calcular la Máxima Utilidad Esperada SIN información ---
        eu_sin_info = {
            accion: self._calcular_eu(accion, self.p_inicial)
            for accion in self.nombres_acciones
        }
        meu_sin_info = max(eu_sin_info.values())
        
        # --- 2. Calcular la Utilidad Esperada CON información ---
        eu_con_info = 0
        for evidencia, prob_evidencia in self.p_evidencia.items():
            # Para cada posible evidencia, encontrar la mejor acción a tomar.
            p_estado_dada_evidencia = self.p_condicional[evidencia]
            
            meu_dada_evidencia = max(
                self._calcular_eu(accion, p_estado_dada_evidencia)
                for accion in self.nombres_acciones
            )
            # Ponderar la utilidad de esa mejor acción por la probabilidad de la evidencia.
            eu_con_info += prob_evidencia * meu_dada_evidencia

        # --- 3. Calcular el Valor de la Información (VOI) ---
        voi = eu_con_info - meu_sin_info
        
        return {
            "meu_sin_info": meu_sin_info,
            "eu_con_info": eu_con_info,
            "voi": voi
        }

# --- 1. DEFINICIÓN UNIFICADA DEL PROBLEMA ---
# Agrupar todos los parámetros en una sola estructura de datos.
PROBLEMA_INVERSION = {
    'probabilidades_iniciales': {'Favorable': 0.6, 'Desfavorable': 0.4},
    'utilidades': {
        'Invertir': {'Favorable': 100, 'Desfavorable': -50},
        'No Invertir': {'Favorable': 0, 'Desfavorable': 0}
    },
    'probabilidades_evidencia': {'Positivo': 0.5, 'Negativo': 0.5},
    'probabilidades_condicionales': {
        'Positivo': {'Favorable': 0.8, 'Desfavorable': 0.2}, # P(Estado | Informe Positivo)
        'Negativo': {'Favorable': 0.2, 'Desfavorable': 0.8}  # P(Estado | Informe Negativo)
    }
}

# --- 2. EJECUCIÓN DEL ANÁLISIS ---
analizador = AnalizadorVOI(PROBLEMA_INVERSION)
resultados = analizador.calcular_voi()

# --- 3. PRESENTACIÓN DE RESULTADOS ---
print("--- Análisis del Valor de la Información (VOI) ---")
print(f"1. Máxima Utilidad Esperada (MEU) sin información: {resultados['meu_sin_info']:.2f}")
print(f"2. Utilidad Esperada (EU) con información perfecta: {resultados['eu_con_info']:.2f}")
print("-" * 50)
print("VOI = EU(con info) - MEU(sin info)")
print(f"VOI = {resultados['eu_con_info']:.2f} - {resultados['meu_sin_info']:.2f} = {resultados['voi']:.2f}")

if resultados['voi'] > 0:
    print(f"\nConclusión: Vale la pena obtener la información, ya que aumenta la utilidad esperada en {resultados['voi']:.2f} puntos.")
else:
    print("\nConclusión: No vale la pena pagar por la información, ya que no mejora la decisión.")