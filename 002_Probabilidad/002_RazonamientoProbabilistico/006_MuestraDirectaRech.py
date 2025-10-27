# =========================================================================
# Inferencia Aproximada con Muestreo por Rechazo (Versión Orientada a Objetos)
# El Muestreo por Rechazo utiliza el Muestreo Directo como subrutina.
# =========================================================================

import random

class MuestreadorDeRed:
    """
    Representa una Red Bayesiana y puede realizar inferencia aproximada
    utilizando Muestreo por Rechazo.
    """

    def __init__(self, modelo_probabilistico):
        """
        Inicializa el muestreador con las Tablas de Probabilidad Condicional (CPTs).
        """
        self.p_lluvia = modelo_probabilistico['Lluvia']
        self.p_aspersor = modelo_probabilistico['Aspersor']
        self.p_humedo_dado_lluvia_aspersor = modelo_probabilistico['Humedo']
        print("Muestreador inicializado con el modelo de la red.")

    def _generar_muestra_directa(self):
        """
        Genera una única muestra completa de la red siguiendo el orden topológico.
        Esta es la subrutina de "Muestreo Directo".
        """
        # 1. Muestrear la variable raíz 'Lluvia' (R).
        lluvia = 'Si' if random.random() < self.p_lluvia else 'No'
        
        # 2. Muestrear la variable raíz 'Aspersor' (S).
        aspersor = 'Si' if random.random() < self.p_aspersor else 'No'
        
        # 3. Muestrear la variable 'Humedo' (W) condicionada a sus padres.
        prob_humedo_si = self.p_humedo_dado_lluvia_aspersor[(lluvia, aspersor)]
        humedo = 'Si' if random.random() < prob_humedo_si else 'No'
        
        # Devuelve la muestra como un diccionario para mayor claridad.
        return {'Lluvia': lluvia, 'Aspersor': aspersor, 'Humedo': humedo}

    def muestreo_por_rechazo(self, var_consulta, evidencia, num_muestras):
        """
        Estima la probabilidad P(Consulta | Evidencia) generando muestras y
        descartando (rechazando) aquellas que no son consistentes con la evidencia.
        """
        conteo_evidencia = 0 # Contador para las muestras que coinciden con la evidencia.
        conteo_consulta = 0  # Contador para las muestras que coinciden con la consulta Y la evidencia.

        for _ in range(num_muestras):
            # a) Generar una muestra completa usando Muestreo Directo.
            muestra = self._generar_muestra_directa()
            
            # b) Comprobar si la muestra es consistente con la evidencia.
            # ej. ¿muestra['Humedo'] es igual a 'Si'?
            es_consistente = all(muestra[var] == val for var, val in evidencia.items())
            
            if es_consistente:
                # c) Si la muestra es consistente (no se rechaza), se acepta.
                conteo_evidencia += 1
                
                # d) Se comprueba si la muestra aceptada también satisface la consulta.
                # ej. ¿muestra['Lluvia'] es igual a 'Si'?
                if muestra[var_consulta[0]] == var_consulta[1]:
                    conteo_consulta += 1
        
        # e) La probabilidad final es el ratio de las cuentas.
        if conteo_evidencia == 0:
            return 0.0, conteo_evidencia # Evitar división por cero.
            
        probabilidad = conteo_consulta / conteo_evidencia
        return probabilidad, conteo_evidencia

# --- 1. DEFINICIÓN DEL MODELO DE LA RED ---
MODELO_PROBABILISTICO = {
    'Lluvia': 0.2,
    'Aspersor': 0.1,
    'Humedo': { # P(Humedo='Si' | Lluvia, Aspersor)
        ('Si', 'Si'): 0.99,
        ('Si', 'No'): 0.90,
        ('No', 'Si'): 0.90,
        ('No', 'No'): 0.01
    }
}

# --- 2. CONFIGURACIÓN DE LA INFERENCIA ---
# La pregunta que queremos responder: P(Lluvia='Si' | Humedo='Si')
VARIABLE_CONSULTA = ('Lluvia', 'Si')
EVIDENCIA = {'Humedo': 'Si'}
NUM_MUESTRAS_TOTALES = 100000

# --- 3. EJECUCIÓN ---
# Se crea una instancia del muestreador con el modelo.
muestreador = MuestreadorDeRed(MODELO_PROBABILISTICO)

# Se ejecuta el algoritmo de Muestreo por Rechazo.
prob_aprox, muestras_validas = muestreador.muestreo_por_rechazo(VARIABLE_CONSULTA, EVIDENCIA, NUM_MUESTRAS_TOTALES)

# --- 4. RESULTADOS ---
print(f"\n--- Inferencia con Muestreo por Rechazo ---")
print(f"Consulta: P({VARIABLE_CONSULTA[0]}={VARIABLE_CONSULTA[1]} | {list(EVIDENCIA.keys())[0]}={list(EVIDENCIA.values())[0]})")
print(f"Total de muestras generadas: {NUM_MUESTRAS_TOTALES}")
print(f"Muestras aceptadas (consistentes con la evidencia): {muestras_validas}")
print(f"Tasa de rechazo: {1 - (muestras_validas / NUM_MUESTRAS_TOTALES):.2%}")
print("-" * 50)
print(f"Probabilidad aproximada: {prob_aprox:.4f}")