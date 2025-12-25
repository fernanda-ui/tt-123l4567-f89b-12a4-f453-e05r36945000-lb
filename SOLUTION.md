EXPLICACION A SOLUCIONES

## PROBLEMA A

Antes de implementar la solucion en codigo, planteo el razonamiento de manera conceptual.

Idea general: 

-- El numero minimo de salas necesarias corresponde al maximo numero de reuniones que estan activas en un mismo momento --


Enfoque de la solucion:

1. Miro todas las horas donde empiezan las reuniones 
2. Miro todas las horas donde terminan las reuniones
3. Avanzamos en el tiempo:
 - Cuando una reunion empieza -> aumenta el numero de reuniones activas 
 - Cuando una reunion termina -> disminuye

4. Se guarda el maximo numero de reuniones activas que hubo en algun momento. (Ese maximo seria la repsuesta)


Pseudocodigo: 

funcion  minimoSalasReuniones(reuniones):

  crear lista de eventos vacia

  para cada reunion en reuniones:
    agregar (horaInicio, +1) a eventos
    agregar (horaFin, -1) a eventos

  ordenar eventos por hora
  si dos eventos tienen la misma hora: 
    procesar primero los eventos de fin

  reuActivas = 0
  maxReuniones = 0

  para cada evento en eventos: 
    reuActivas = reuActivas + cambio
    si reuActivas > maxReuniones:
    maxReuniones = reuActivas

retornar maxReuniones


Explicacion: 

Lo primero que hacemos es crear una lista donde se almacenaran todos los eventos relevantes, estos eventos representan momentos en los que una reunion empieza o termina, como por ejemplo: 

- a las 9:30 empieza una reunion
- a las 11:00 termina una reunion

Cada evento tiene una hora y un cambio: 

+1 (sumar una al contador) si comienza una reunion
-1 (restar una del contador) si termina una reunion 

Posteriormente, se ordenan los eventos cronológicamente por hora. Como condicion, que si dos eventos ocurren a la misma hora, primero se debe procesar los eventos de finalización y luego los de inicio; asi se evita contar como solapadas aquellas reuniones que terminan exactamente cuando otras comienzan.

Finalmente, se recorre la lista de eventos simulando el avance del tiempo, contando cuantas reuniones están activas en cada momento y almacenando el valor maximo alcanzado.  

Ese valor maximo corresponde al número minimo de salas necesarias.

Codigo -> (MinSalas.py)


**Pruebas (Testing)**

- Ejecución de las Pruebas:

```bash
# Ejecutar todos los tests con reporte detallado
python -m pytest tests/testMinSalidas.py -v

# Resultado esperado:
# 5 funciones ejecutadas
# 25 asserts verificados
# 100% de tests pasados
```

Para validar la correctitud del algoritmo, se implementaron pruebas unitarias exhaustivas usando pytest.

Estructura de las Pruebas: 

Se crearon 5 funciones de test que verifican 25 casos diferentes:

1. Tests sin solapamientos (4 casos)
Validan que el algoritmo identifique correctamente cuándo las reuniones NO se superponen:
- Reuniones consecutivas (una termina cuando otra empieza)
- Reuniones con espacios entre ellas
- Una sola reunión
- Reuniones desordenadas sin solapamiento

Resultado esperado: 1 sala es suficiente

2. Tests con solapamientos (6 casos)
Verifican que el algoritmo maneje correctamente reuniones que se superponen:
- Dos reuniones solapadas parcialmente
- Tres o más reuniones solapadas
- Todas las reuniones al mismo tiempo
- Una reunión larga que contiene otras más pequeñas
- Solapamientos escalonados
- Picos de máxima concurrencia

Resultado esperado: 2-3 salas según el caso

3. Tests de casos borde (6 casos)
Evaluan situaciones límite críticas:
- Reunión que empieza exactamente cuando otra termina
- Múltiples reuniones consecutivas en el mismo punto
- Combinación de bordes con solapamientos
- Reuniones de duración cero
- Múltiples puntos de inicio/fin coincidentes

Resultado esperado: Manejo correcto de igualdad temporal

4. Tests de rendimiento (4 casos)
Prueban el algoritmo con conjuntos grandes de datos:
- 100 reuniones consecutivas
- 50 reuniones simultáneas
- 100 reuniones con solapamiento gradual
- 200 reuniones mixtas

Resultado esperado: Ejecución rápida y correcta con muchos datos

5. Tests adicionales (5 casos)
Casos especiales y validaciones extras:
- Lista vacia (0 reuniones)
- Horarios con decimales (ej: 8.5, 9.5)
- Reuniones al inicio y fin del dia
- Reuniones que empiezan juntas pero terminan en diferentes momentos
- Reuniones que terminan juntas pero empiezan en diferentes momentos


**Cobertura de Casos**

Las pruebas cubren:
- Casos sin solapamientos  
- Casos con solapamientos  
- Casos de borde (horaInicio == horaFin)  
- Rendimiento con muchas reuniones  
- Validación de datos (lista vacía, horarios decimales)  

**Verificación de Correctitud**

Todos los tests pasaron exitosamente, confirmando que:
- El algoritmo maneja correctamente reuniones sin solapamiento
- Calcula el máximo de reuniones simultáneas correctamente
- Procesa correctamente el caso borde donde una termina cuando otra empieza
- Es eficiente con grandes cantidades de datos
- Maneja casos especiales y límite sin errores

**Errores Encontrados y Soluciones**

Durante la implementación y ejecución de los tests, se identificaron y corrigieron los siguientes errores:

- Error 1: Expectativa incorrecta en solapamientos escalonados

Descripción del error:
```python
# Test original (incorrecto)
reuniones5 = [(8, 10), (9, 11), (10, 12), (11, 13), (12, 14)]
assert minimoSalasReuniones(reuniones5) == 3  #FALLÓ
```

Problema identificado:
Se esperaba que este caso requiriera 3 salas, pero el algoritmo correctamente devolvió 2.

Análisis:
- Reunión 1: [8-10]
- Reunión 2: [9-11] (se solapa con 1)
- Reunión 3: [10-12] (empieza cuando 1 termina, se solapa con 2)
- Reunión 4: [11-13] (empieza cuando 2 termina, se solapa con 3)
- Reunión 5: [12-14] (empieza cuando 3 termina, se solapa con 4)

Máximo en un momento: En cualquier punto del tiempo, máximo hay 2 reuniones simultáneas.

Solución aplicada:
```python
# Test corregido
reuniones5 = [(8, 10), (9, 11), (10, 12), (11, 13), (12, 14)]
assert minimoSalasReuniones(reuniones5) == 2  # CORRECTO
```

Lección aprendida:
Es crucial verificar manualmente los casos de prueba antes de asumir el resultado esperado. Este error demostró que el algoritmo funciona correctamente y el problema estaba en la expectativa del test.


- Error 2: Cálculo incorrecto con horarios decimales

Descripción del error:
```python
# Test original (incorrecto)
reuniones2 = [(8.5, 9.5), (9, 10), (9.5, 10.5)]
assert minimoSalasReuniones(reuniones2) == 3  #FALLÓ
```

Problema identificado:
Se esperaban 3 salas simultáneas, pero el análisis mostró que solo se necesitan 2.

Análisis detallado por tiempo:
- 8:30 - 9:00: 1 reunión activa [(8.5, 9.5)]
- 9:00 - 9:30: 2 reuniones activas [(8.5, 9.5), (9, 10)]
- 9:30 - 10:00: 2 reuniones activas [(9, 10), (9.5, 10.5)] ← Máximo = 2
- 10:00 - 10:30: 1 reunión activa [(9.5, 10.5)]

Nunca hay 3 reuniones al mismo tiempo, el pico es de 2.

Solución aplicada:
```python
# Test corregido
reuniones2 = [(8.5, 9.5), (9, 10), (9.5, 10.5)]
assert minimoSalasReuniones(reuniones2) == 2  # CORRECTO
```

Lección aprendida: 
Los horarios decimales pueden confundir visualmente. Es recomendable dibujar una línea de tiempo o simular manualmente el algoritmo para verificar casos complejos.


- Error 3: Importación de módulo en pytest

Descripción del error:
```bash
ModuleNotFoundError: No module named 'MinSalas'
```

Problema identificado:
pytest no encontraba el módulo `MinSalas` porque está en la carpeta `src/` y no en el `PYTHONPATH`.

Solución aplicada:
Crear el archivo `pytest.ini` con la configuración:
```
[pytest]
pythonpath = src
```

Lección aprendida:
Para proyectos con estructura de carpetas (`src/`, `tests/`), es necesario configurar pytest con un archivo `pytest.ini` o `pyproject.toml` para que encuentre los módulos correctamente.


**Uso de Inteligencia Artificial**

Durante el desarrollo de este proyecto, se utilizaron dos herramientas de IA en diferentes etapas del proceso:

- ChatGPT 5.2 - Para fundamentación teórica y conceptos algorítmicos
- GitHub Copilot (Claude Sonnet 4.5) - Integrado en VS Code para implementación y testing 

A continuación se detalla cómo se aplicó cada herramienta de IA y qué aportes fueron más valiosos.

1. ChatGPT 5.2

Áreas donde se utilizó:

- Fundamentación Teórica y Diseño del Algoritmo

Prompt utilizado:
> "Necesito resolver el problema de determinar el número mínimo de salas de reuniones necesarias dadas varias reuniones con horarios de inicio y fin. ¿Qué enfoque algorítmico me recomiendas?"

Aporte de la IA:
- Explicó el enfoque de "línea de barrido" (sweep line) para resolver el problema
- Sugirió usar eventos de inicio (+1) y fin (-1) de reuniones
- Proporcionó el razonamiento conceptual de por qué funciona este enfoque
- Explicó la importancia del ordenamiento y manejo de casos borde

Valor agregado:  
La IA me ayudó a comprender la lógica fundamental del algoritmo antes de implementarlo, lo cual fue crucial para escribir código limpio desde el principio.


2. GitHub Copilot (Claude Sonnet 4.5)

Áreas donde se utilizó

- Implementación y Optimización del Código

Prompts utilizados:
> "¿Cómo ordeno correctamente los eventos cuando dos reuniones tienen el mismo horario?"
> 
> "¿Por qué debo procesar los eventos de fin antes que los de inicio cuando ocurren al mismo tiempo?"

Aporte de la IA:
- Explicó que al ordenar por `(hora, tipo_evento)`, el `-1` (fin) va antes que el `+1` (inicio)
- Aclaró que esto evita contar como solapadas las reuniones que terminan exactamente cuando otras empiezan
- Sugirió usar `lambda x: (x[0], x[1])` para el ordenamiento

Código resultante:
```python
eventos.sort(key=lambda x: (x[0], x[1]))
```

Valor agregado:
Esta sugerencia fue crítica para manejar correctamente los casos borde, uno de los requisitos más importantes del problema.

- Diseño e Implementación de Tests

Prompts utilizados:
> "Necesito implementar tests que cubran: casos sin solapamientos, casos con solapamientos, casos de borde (horaInicio == horaFin), y pruebas de rendimiento"
> "¿Qué casos específicos debería incluir para probar el manejo de casos borde?"
> "Cómo configuro pytest para que encuentre módulos en la carpeta src/"

Aportes de la IA:
Estructura de tests: Sugirió organizar los tests en funciones separadas por categoría.
Casos específicos: Recomendó probar:
   Reuniones consecutivas sin espacios
   Múltiples reuniones terminando/iniciando al mismo tiempo
   Reuniones con horarios decimales
   Lista vacía y casos extremos
Configuración de pytest: Proporcionó la solución del archivo `pytest.ini`
 

Ejemplo de test mejorado con sugerencia de IA:
```python
# Sin mensaje (antes)
assert minimoSalasReuniones(reuniones1) == 1

# Con mensaje descriptivo (después)
assert minimoSalasReuniones(reuniones1) == 1, "Reuniones consecutivas deben usar 1 sala"
```

Valor agregado:
La IA me ayudó a pensar en casos de prueba que no había considerado inicialmente, mejorando significativamente la cobertura de testing.


- Debugging y Corrección de Errores

Prompts utilizados:
> "Mi test falla con reuniones [(8, 10), (9, 11), (10, 12), (11, 13), (12, 14)]. Esperaba 3 salas pero devuelve 2. ¿Está mal el algoritmo o el test?"
> "pytest no encuentra el módulo MinSalas. ¿Cómo lo soluciono?"

Aportes de la IA:
Análisis de expectativas incorrectas: Explicó paso a paso por qué el algoritmo estaba correcto y el test tenía un valor esperado equivocado.
Solución de configuración: Proporcionó la solución con `pytest.ini` para el problema de importación.
Explicación de PYTHONPATH: Aclaró conceptos sobre cómo Python busca módulos.

Valor agregado:
La IA funcionó como un "segundo par de ojos" para identificar errores en las expectativas de los tests, no en el algoritmo.


## PROBLEMA B

Idea general:

La caché es como una cajita con espacio limitado donde guardamos datos para usarlos rapido.

Pero esa cajita tiene dos reglas importantes:

1. Regla del tiempo (TTL)
  - Cada dato que entra a la caché tiene una fecha de vencimiento.
  - Si pasa ese tiempo:
    - el dato ya no sirve
    - se elimina automáticamente
  - No importa si ese dato se usó mucho antes: si venció, se va

Ademas: 
- Cada vez que usamos un dato (con Get o Set)
- su tiempo de vida se renueva

Es como decir: si usas algo, le doy mas tiempo de vida

2. Regla del espacio (LRU)

- La caché tiene un límite de espacio
- Si está llena y quiero guardar algo nuevo:
  - debo sacar uno viejo
- ¿Cuál saco?
  - El que hace más tiempo no se usa

Es como limpiar una mochila: si está llena, botas lo que llevas más tiempo sin usar

3. ¿Qué hay que calcular realmente?

Es un control de estado:
- Qué claves existen
- Cuáles ya expiraron
- Cuáles se usaron más recientemente
- Cuándo eliminar algo por:
tiempo (TTL)
espacio (LRU)

4. Conclusión: 
La solución consiste en mantener una estructura en memoria que almacene cada clave con su tiempo de expiración y su último uso.
Antes de devolver o agregar datos, se eliminan las entradas expiradas.
Cuando se supera la capacidad, se expulsa la entrada menos recientemente utilizada.


Codigo -> (CacheMemory.py)


**Estructura de Datos**

La implementación utiliza un diccionario de Python como estructura principal:

```python
self.data = {
    "clave1": {
        "value": "valor1",
        "expiration_time": 1735000000.0,  # timestamp Unix
        "last_used": 1734999000.0          # timestamp Unix
    },
    "clave2": { ... }
}
```

Justificación:
- Acceso O(1) para operaciones get/set/delete
- Fácil iteración para encontrar LRU
- Almacenamiento de metadata junto con el valor


**Manejo de TTL (Time To Live)**

Implementación:
1. Al agregar/actualizar una entrada: `expiration_time = now + DefaultTtlSeconds`
2. Al consultar: Se verifica si `expiration_time < now`
3. Si expiró: Se elimina y retorna `None`
4. Si es válida: Se renueva el TTL (comportamiento requerido)

Limpieza proactiva:
- `remove_expired()` se llama antes de operaciones críticas
- Previene que entradas expiradas ocupen espacio innecesariamente
- Incrementa contador de estadísticas


**Manejo de LRU (Least Recently Used)**

Implementación:
1. Cada entrada tiene `last_used` actualizado en cada uso
2. Cuando `len(self.data) >= capacity`:
   - Se busca la clave con `last_used` más antiguo
   - Se elimina esa clave
   - Se incrementa contador de estadísticas


Complejidad:
- Búsqueda LRU: O(n) donde n = número de entradas
- Trade-off aceptable para capacidades pequeñas/medianas


**Estadísticas (Stats - BONUS)**

Se implementó el método `stats()` que retorna:

```python
{
    "total_calls": 150,      # Llamadas a get() y set()
    "total_keys": 10,        # Claves actuales (no expiradas)
    "ttl_expired": 25,       # Claves eliminadas por TTL
    "lru_evicted": 15        # Claves expulsadas por LRU
}
```

Utilidad:
- Monitoreo de uso de la caché
- Detección de problemas (muchas expulsiones LRU = capacidad insuficiente)
- Métricas para optimización


**Alternativas de Solución Consideradas**

- Alternativa 1: OrderedDict para LRU

Descripción:
Usar `collections.OrderedDict` que mantiene orden de inserción automáticamente.

Ventajas:
- LRU más eficiente: O(1) para mover al final
- Código más simple para LRU

Desventajas:
- No maneja TTL nativamente
- Requiere lógica adicional para expiración
- Menos flexible para metadata personalizada

Por qué se descartó:
La necesidad de manejar TTL con timestamps y metadata adicional hace que un diccionario simple sea más flexible. La pérdida de eficiencia en LRU (O(n) vs O(1)) es aceptable para capacidades moderadas.


- Alternativa 2: Redis o Base de Datos en Memoria

Descripción: 
Usar herramientas externas como Redis que tienen TTL y LRU nativos.

Ventajas:
- TTL y LRU altamente optimizados
- Persistencia incluida
- Escalabilidad

Desventajas:
- Dependencia externa
- Sobrecarga para casos simples
- No cumple requisito de "caché en memoria" implementada por uno mismo

Por qué se descartó:
El problema pide implementar una caché, no usar una existente. Redis sería ideal para producción pero no para este ejercicio.



**Optimizaciones Posibles**

1. Usar OrderedDict + Custom TTL

Implementación:

```python
from collections import OrderedDict

class OptimizedCache:
    def __init__(self, capacity, ttl):
        self.cache = OrderedDict()
        self.ttl_data = {}  # key -> expiration_time
```

Beneficio:
- LRU: O(1) con `move_to_end()`
- Mantiene compatibilidad con TTL

Trade-off:
- Más complejo de mantener
- Dos estructuras de datos


2. Lazy Deletion (Eliminación Perezosa)

Concepto:
No limpiar entradas expiradas hasta que sean accedidas.

Implementación actual:
```python
# Limpieza proactiva
self.remove_expired()  # Se llama en cada operación
```

Optimización:
```python
# Limpieza perezosa
# Solo verificar al acceder específicamente a una clave
```

Beneficio:
- Menos operaciones de limpieza
- Mejor rendimiento promedio

Trade-off:
- Claves expiradas ocupan memoria más tiempo
- `keys_and_values()` puede ser más lento


3. Índice LRU con Heap

Implementación:

```python
import heapq

class CacheWithHeap:
    def __init__(self, capacity, ttl):
        self.data = {}
        self.lru_heap = []  # (last_used, key)
```

Beneficio:
- Búsqueda LRU: O(log n)
- Mejor escalabilidad

Costo:
- Complejidad de código
- Memoria adicional



**Decisiones de Diseño Justificadas**

1. Por qué diccionario simple
- Simplicidad y claridad
- O(1) para operaciones principales
- Fácil de entender y mantener
- Suficiente para casos de uso típicos

2. Por qué limpieza proactiva
- Evita que expirados consuman capacidad
- `keys_and_values()` siempre retorna datos válidos
- Facilita testing y debugging

3. Por qué estadísticas separadas
- No afecta rendimiento (simples contadores)
- Valiosas para monitoreo
- Cumplen bonus solicitado

 4. Por qué no thread-safe por defecto
- YAGNI: No requerido explícitamente
- Evita overhead innecesario
- Fácil de agregar si se necesita

**Casos de Uso Ideales**

Esta implementación es ideal para:
- Cachés de aplicación con capacidad < 10,000 entradas
- Datos que expiran naturalmente (sesiones, tokens)
- Aplicaciones single-threaded
- Prototipos y pruebas de concepto

No es ideal para:
- Cachés masivas (> 100,000 entradas)
- Alta concurrencia sin modificaciones
- Persistencia crítica (sin implementar)
- Distribución entre servidores
---

**Pruebas (Testing)**

Comando de Ejecución

Opcion 1:
$env:PYTHONPATH="src"; python tests\testCacheMemory.py

Opcion 2:
python -m pytest tests/testCacheMemory.py -v


Para validar la correctitud de la implementación de CacheMemory, se crearon 16 funciones de test exhaustivas usando Python y pytest.

- Estructura de las Pruebas

Las pruebas se organizaron en 6 categorías principales:

1. Tests de Operaciones Básicas (5 tests)

Objetivo: Verificar que las operaciones CRUD funcionan correctamente.

- test_agregar_entradas_nuevas: Valida que se pueden agregar múltiples entradas hasta la capacidad máxima
- test_actualizar_entradas_existentes: Verifica que actualizar una clave existente sobrescribe el valor
- test_eliminar_entradas: Confirma que `delete()` retorna `True`/`False` según corresponda
- test_leer_entradas_validas: Valida que `get()` retorna valores correctos
- test_leer_entradas_inexistentes: Verifica que `get()` retorna `None` para claves inexistentes

Resultado esperado: Operaciones básicas funcionan correctamente.

2. Tests de TTL - Time To Live (3 tests)

Objetivo: Validar el comportamiento de expiración temporal.

- test_leer_entradas_expiradas: Verifica que las entradas expiran después del tiempo configurado
  - Usa `time.sleep(2.5)` con TTL=2 segundos
  - Confirma que `get()` retorna `None` para entradas expiradas
  
- test_actualizacion_ttl_al_usar: Valida el requisito crítico: "Get cuenta como uso y renueva el TTL"
  - Agrega entrada con TTL=3s
  - Espera 2s, usa la clave (renueva TTL)
  - Espera otros 2s (total 4s pero TTL renovado)
  - Verifica que sigue existiendo
  
- test_actualizacion_ttl_con_set Confirma que `set()` también renueva el TTL al actualizar

Resultado esperado: TTL funciona correctamente con renovación en uso.

3. Tests de LRU - Least Recently Used (2 tests)

Objetivo: Validar la expulsión de entradas menos usadas.

- test_expulsion_por_lru: Caso básico
  - Caché capacidad=3
  - Llena con key1, key2, key3
  - Agrega key4 (debe expulsar key1 por ser la menos usada)
  
- test_expulsion_lru_con_uso_intermedio: Caso complejo
  - Caché capacidad=3
  - Agrega a, b, c
  - Usa `get(a)` → actualiza last_used de 'a'
  - Usa `get(c)` → actualiza last_used de 'c'
  - Agrega 'd' → debe expulsar 'b' (menos recientemente usada)
  - Verifica que a, c, d existen pero b no

Resultado esperado: LRU expulsa correctamente basado en `last_used`

4. Test de Listado (1 test)

Objetivo: Validar el método `keys_and_values()`.

- test_listar_todas_las_entradas:
  - Caché vacía retorna `[]`
  - Agrega múltiples entradas
  - Verifica que retorna lista de tuplas `(key, value)`
  - Confirma que limpia expirados antes de listar

Resultado esperado: Listado funciona y excluye expirados

5. Tests de Estadísticas - BONUS (3 tests)

Objetivo: Validar el método `stats()` implementado como bonus.

- test_estadisticas_basicas: 
  - Verifica contadores iniciales en 0
  - Realiza operaciones (2 set + 1 get)
  - Confirma `total_calls = 3`
  - Verifica `total_keys = 2`
  
- test_estadisticas_ttl_expired:
  - Agrega entradas con TTL corto
  - Espera expiración
  - Lee entrada (detecta expiración)
  - Verifica que `ttl_expired >= 1`
  
- test_estadisticas_lru_evicted:
  - Caché capacidad=2
  - Fuerza 2 expulsiones LRU
  - Verifica que `lru_evicted = 2`

Resultado esperado: Estadísticas cuentan correctamente todas las operaciones

6. Tests de Casos Borde (2 tests)

Objetivo: Probar situaciones extremas y casos límite.

- test_casos_borde:
  - Caché con capacidad mínima (capacity=1)
  - TTL de 0 segundos (expira inmediatamente)
  - Verifica comportamiento correcto en extremos
  
- test_operaciones_mixtas:
  - Combinación de set, get, delete, update
  - Valida que todas las operaciones funcionan juntas

Resultado esperado: Casos extremos manejados correctamente

**Errores Encontrados y Soluciones**

Durante la implementación y testing, no se encontraron errores en la lógica principal. La implementación funcionó correctamente desde el inicio. 


**Uso de Inteligencia Artificial**

Durante el desarrollo del Problema B (CacheInMemory), se utilizaron dos herramientas de IA en diferentes etapas del proceso:

- ChatGPT 5.2 - Para diseño conceptual y alternativas de implementación
- GitHub Copilot (Claude Sonnet 4.5) - Integrado en VS Code para implementación y testing

A continuación se detalla cómo se aplicó cada herramienta de IA y qué aportes fueron más valiosos.

1. ChatGPT 5.2

Áreas donde se utilizó:

- Diseño Conceptual de la Caché

Prompt utilizado:
> "Necesito implementar una caché en memoria con TTL (Time To Live) y política de expulsión LRU (Least Recently Used). ¿Qué estructura de datos me recomiendas y cómo debería manejar la expiración temporal?"

Aporte de la IA:
- Explicó las diferencias entre TTL y LRU como mecanismos de expulsión
- Sugirió usar un diccionario con metadata (expiration_time, last_used)
- Proporcionó el concepto de "limpieza proactiva vs perezosa"
- Explicó por qué OrderedDict puede ser mejor para LRU pero menos flexible para TTL

Valor agregado:
La IA me ayudó a entender que TTL y LRU no son mutuamente excluyentes, sino complementarios. TTL elimina por tiempo, LRU elimina por espacio.


- Análisis de Alternativas

Prompt utilizado:
> "¿Cuáles son las ventajas y desventajas de usar un diccionario simple vs OrderedDict vs una solución con heap para implementar LRU?"

Aporte de la IA:
- Comparó complejidades temporales: O(n) vs O(1) vs O(log n)
- Explicó trade-offs entre simplicidad y eficiencia
- Recomendó empezar simple y optimizar si es necesario
- Sugirió que para capacidades < 10,000 entradas, O(n) es aceptable

Valor agregado:
Me ayudó a tomar decisiones de diseño justificadas en lugar de elegir arbitrariamente una estructura de datos.


2. GitHub Copilot (Claude Sonnet 4.5)

Áreas donde se utilizó:

- Implementación del Método remove_expired()

Prompts utilizados:
> "Cómo elimino todas las entradas expiradas de la caché antes de hacer operaciones?"
> "Necesito incrementar un contador cada vez que se elimina una entrada por TTL"

Aporte de la IA:
- Sugirió iterar sobre una copia de las claves: `list(self.data.keys())`
- Explicó por qué no se puede modificar un diccionario mientras se itera
- Proporcionó el código para comparar timestamps: `expiration_time < self.current_time()`

Valor agregado:
Esta implementación evitó el error común de "dictionary changed size during iteration". La IA anticipó este problema.


- Implementación del Método remove_lru()

Prompts utilizados:
> "Cómo encuentro la entrada menos recientemente usada en mi caché?"
> "Quiero expulsar la entrada con el last_used más antiguo"

Aporte de la IA:
- Sugirió usar `min()` con una función key personalizada
- Proporcionó: `min(self.data.items(), key=lambda item: item[1]["last_used"])`
- Explicó que esto retorna la tupla (clave, valor) con menor last_used
- Recordó incrementar el contador de expulsiones LRU

Valor agregado:
Código elegante y eficiente en 3 líneas. Sin la IA, probablemente hubiera usado un loop manual menos eficiente.


- Renovación de TTL al Usar

Prompts utilizados:
> "El requisito dice que Get cuenta como uso y renueva el TTL. ¿Cómo implemento eso?"
> "Si hago Set a una clave existente, ¿también renuevo el TTL?"

Aporte de la IA:
- Aclaró que "renovar TTL" significa recalcular `expiration_time = now + ttl`
- Confirmó que tanto `get()` como `set()` deben renovar el TTL
- Sugirió actualizar `last_used` y `expiration_time` juntos
- Explicó que esto hace que las entradas activas "nunca expiren"

Valor agregado:
La IA clarificó un requisito que podría haber interpretado mal. "Renovar TTL" no significa extender, sino resetear completamente.


- Diseño e Implementación de Tests

Prompts utilizados:
> "Necesito tests completos para validar: operaciones CRUD, TTL con expiración, LRU con expulsión, renovación de TTL al usar, y estadísticas"
> "¿Cómo pruebo que el TTL se renueva correctamente al usar get()?"
> "¿Qué casos borde debo considerar para la caché?"

Aportes de la IA:
- Estructura de 6 categorías: CRUD, TTL, LRU, Listado, Estadísticas, Casos Borde
- Sugirió usar `time.sleep()` para simular paso del tiempo
- Recomendó agregar márgen de seguridad: `sleep(2.5)` para TTL=2s
- Advirtió sobre test complejo de renovación TTL
- Sugirió test de expulsión LRU con uso intermedio para validar que `last_used` se actualiza correctamente

Valor agregado:
Los tests propuestos por la IA cubrieron casos que no había considerado, especialmente el comportamiento de renovación de TTL.
