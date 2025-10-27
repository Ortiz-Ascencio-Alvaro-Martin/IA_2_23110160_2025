# =========================================================================
# Algoritmo Evolutivo (Implementación Orientada a Objetos de un AG)
# Objetivo: Evolucionar una población de secuencias binarias hasta
#           encontrar la secuencia objetivo "11111111".
# =========================================================================

import random

class AlgoritmoEvolutivo:
    """
    Encapsula la lógica completa de un Algoritmo Genético.
    Maneja la población, la selección, el cruce y la mutación para
    evolucionar soluciones a un problema.
    """

    def __init__(self, tamano_secuencia, tamano_poblacion, tasa_mutacion, tamano_torneo=2):
        """
        Inicializa el algoritmo con sus parámetros fundamentales.
        """
        self.tamano_secuencia = tamano_secuencia
        self.tamano_poblacion = tamano_poblacion
        self.tasa_mutacion = tasa_mutacion
        self.tamano_torneo = tamano_torneo # Para el método de selección.

    def _calcular_fitness(self, secuencia):
        """
        Función de aptitud: Mide qué tan "buena" es una solución.
        En este caso, es simplemente la cantidad de '1's en la secuencia.
        """
        return sum(secuencia)

    def _inicializar_poblacion(self):
        """
        Crea la primera generación de soluciones de forma completamente aleatoria.
        """
        return [[random.randint(0, 1) for _ in range(self.tamano_secuencia)] for _ in range(self.tamano_poblacion)]

    def _seleccion_por_torneo(self, poblacion_evaluada):
        """
        Método de Selección por Torneo: Elige a los mejores de un subgrupo aleatorio.
        Es una alternativa eficiente a la selección por ruleta.
        """
        # 1. Se eligen 'k' individuos al azar de la población para el torneo.
        participantes = random.sample(poblacion_evaluada, self.tamano_torneo)
        
        # 2. Se ordenan los participantes por su fitness (de mejor a peor).
        participantes.sort(key=lambda item: item[1], reverse=True)
        
        # 3. El individuo con el mejor fitness gana el torneo y es seleccionado como padre.
        return participantes[0][0]

    def _cruce_en_un_punto(self, padre1, padre2):
        """
        Crossover: Combina el material genético de dos padres para crear un hijo.
        """
        # Se elige un punto aleatorio para cortar las secuencias.
        punto_de_corte = random.randint(1, self.tamano_secuencia - 1)
        
        # El hijo hereda la primera parte del padre1 y la segunda del padre2.
        hijo = padre1[:punto_de_corte] + padre2[punto_de_corte:]
        return hijo

    def _mutar(self, secuencia):
        """
        Mutación: Introduce pequeños cambios aleatorios en la secuencia de un hijo
        para mantener la diversidad genética.
        """
        for i in range(self.tamano_secuencia):
            if random.random() < self.tasa_mutacion:
                # Se invierte el bit (0 -> 1, 1 -> 0).
                secuencia[i] = 1 - secuencia[i]
        return secuencia

    def ejecutar(self, max_generaciones):
        """
        Orquesta el proceso evolutivo completo durante un número máximo de generaciones.
        """
        # Se crea la población inicial.
        poblacion = self._inicializar_poblacion()
        mejor_solucion_global = None
        mejor_fitness_global = -1

        print("--- Iniciando Proceso Evolutivo (Objetivo: Fitness 8) ---")

        for gen in range(1, max_generaciones + 1):
            
            # 1. EVALUACIÓN: Calcular el fitness de cada individuo en la población.
            poblacion_evaluada = [(individuo, self._calcular_fitness(individuo)) for individuo in poblacion]
            
            # Actualizar la mejor solución encontrada hasta ahora.
            mejor_de_la_gen = max(poblacion_evaluada, key=lambda item: item[1])
            if mejor_de_la_gen[1] > mejor_fitness_global:
                mejor_fitness_global = mejor_de_la_gen[1]
                mejor_solucion_global = mejor_de_la_gen[0]

            # Imprimir estadísticas de la generación actual.
            fitness_promedio = sum(fit for ind, fit in poblacion_evaluada) / self.tamano_poblacion
            print(f"Generación {gen:02d}: Mejor Fitness = {mejor_fitness_global} | Fitness Promedio = {fitness_promedio:.2f}")

            # Condición de parada: si encontramos la solución perfecta.
            if mejor_fitness_global == self.tamano_secuencia:
                print("\n¡Solución óptima encontrada!")
                break

            # 2. CREACIÓN DE LA SIGUIENTE GENERACIÓN
            siguiente_generacion = []
            
            # Elitismo: El mejor individuo de la generación pasa directamente a la siguiente.
            siguiente_generacion.append(mejor_solucion_global)

            # Llenar el resto de la nueva población.
            while len(siguiente_generacion) < self.tamano_poblacion:
                # a. Selección
                padre1 = self._seleccion_por_torneo(poblacion_evaluada)
                padre2 = self._seleccion_por_torneo(poblacion_evaluada)
                
                # b. Cruce
                hijo = self._cruce_en_un_punto(padre1, padre2)
                
                # c. Mutación
                hijo_mutado = self._mutar(hijo)
                
                siguiente_generacion.append(hijo_mutado)
            
            poblacion = siguiente_generacion
        
        return mejor_solucion_global, mejor_fitness_global


# --- Ejecución del Algoritmo ---
# Configuración
TAMANO_SECUENCIA = 8
TAMANO_POBLACION = 5
TASA_MUTACION = 0.05
MAX_GENERACIONES = 15

# 1. Se crea una instancia del algoritmo con nuestros parámetros.
ag = AlgoritmoEvolutivo(TAMANO_SECUENCIA, TAMANO_POBLACION, TASA_MUTACION)

# 2. Se ejecuta el proceso evolutivo.
solucion, fitness = ag.ejecutar(MAX_GENERACIONES)

# 3. Se muestran los resultados finales.
print("-" * 50)
print("Búsqueda finalizada.")
print(f"Mejor Solución: {''.join(map(str, solucion))}")
print(f"Fitness Final: {fitness} / {TAMANO_SECUENCIA}")