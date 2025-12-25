Prueba técnica - Desarrolaldor Junior - 2025-12-24

Desgloce de la prueba

Requesitos:

- Planteamiento algorítmico razonable, logica de soluciones y buenas practicas.
- Especificar herramientas utilizadas (escogiendo el lenguaje de preferencia, permitiendo usar IA)
- Crear un repositorio publico en Github

Estructura solicitada:

`src/`: Código fuente
`tests/`: Pruebas unitarias
`README.md`: Instrucciones generales
`SOLUTION.md`: Explicación de la solución


Problemas planteados:

1. Problema A: Salas de reúnion 
2. Problema B: Caché concurrente en memoria con TTL y LRU


#####################################################################################################

Inicio de la prueba -> 2:20 pm 
Pausa: 6:09 pm - 7:57 pm
Finalización de la prueba -> 11:30 pm

- Problema A: 2:20 pm - 6:09 pm
- Problema B: 7:57 pm - 11:30 pm


Herramientas que se utilizaran: 

- Editor de codigo: Visual Studio Code
- Lenguaje: Python 
- Testing: pytest
- Control de versiones: Git + GitHub
- IA: ChatGPT 5.2
- GitHub Copilot (Claude Sonnet 4.5)

Instalación:

- Asegúrese de tener Python 3.10 o superior instalado.
- (Opcional) Cree y active un entorno virtual.
- Instale las dependencias:
   pip install -r requirements.txt


## PROBLEMA A - Salas de reuniones

Tenemos varias reuniones, donde todas son el mismo dia, cada una con: 

- Hora de inicio
- Hora fin

Tener en cuenta:

- Dos reuniones no pueden usar la misma sala si sus horarios se cruzan
- Se quiere saber cuantas salas como minimo necesitamos para que todas puedan ocurrir


Requisitos:

- Lista de reuniones
- Cada reunion es un par: {horaInicio, horaFin}
- Siempre se cumpla: 
- - horaInicio < horaFin 
- - No hay reuniones de un dia a otro


## PROBLEMA B - Caché en memoria con TTL Y LRU

1. Objetivo: 

Diseñar e implementar una caché en memoria que: 

- Almacene pares clave-valor
- Tenga un limite maximo de capacidad
- Elimina datos automaticamente según:
  - TTL (tiempo de vida)
  - LRU (menos recientemente usado)


2. Restricciones: 

- Capacidad:
  - La caché no puede almacenar mas entradas que el valor definido en capacity.
  - Solo se cuentan las entradas no expiradas. 


TTL (Time To Live)

- Cada entrada tiene un tiempo de vida.
- Al expirar: 
  - La entrada se considera valida
  - Debe eliminarse
  - No puede ser retornada por Get

Reglas importantes:

- El TTL se asigna al crear una entrada
- El TTL se reinicia cada vez que: 
  - Se usa Get
  - Se usa Set sobre esa clave
- Los metodos Get y Set son los unicos que cuentan como uso

LRU (Least Recently Used)

- Aplica solo cuando: 
  - La caché esta llena 
  - Se intenta insertar una nueva entrada valida

- Se elimina la entrada:
  - Menos recientemente usada 
  - Que no haya expirado 

- El uso reciente se define por:
  - Ultimo Get
  - Ultimo Set


3. Operaciones que debe soportar la caché:


Set(key, value)

Debe: 
- Agregar una nueva entrada
- Actualizar una existente 
- Reiniciar su TTL
- Marcarla como recientemente usada
- Si supiera la capacidad:
  - Eliminar entradas expiradas primero
  - Si aun no hay espacio -> aplicar LRU

No retornar ningun valor.

Get(key)

Debe: 
- Verificar si la clave existe
- Verificar si no ha expirado 
- Si expiró:
  - Eliminarla 
  - Retornar null
- Si es valida:
  - Retornar el valor 
  - Reiniciar TTL 
  - Marcarla como recientemente usada

Delete(key) 

Debe: 
- Eliminar la clave si existe
- Retornar:
  - true si fue eliminada 
  - false si no existia

KeysAndValues()

Debe: 
- Retornar todas las claves y valores:
  - Que existan 
  - Que no esten expiradas


4. Manejo del tiempo

- Todas las entradas deben guardar: 
  - Momento de ultima utilizacion 
  - Momento de expiración 
- El tiempo se maneja en segundos 
- No se contemplan cambios de fecha (todo ocurre en tiempo relativo)

5. Concurrencia 

- La caché debe ser segura ante accesos concurrentes
- No deben producirse estados inconsistentes
- Se puede manejar mediante:
  - Exclusión mutua (locks)
  - O estructuras seguras para concurrencia

6. Casos que deben contemplarse

- Agregar claves nuevas
- Actualizar claves existentes
- Eliminar claves
- Obtener claves válidas
- Obtener claves inexistentes
- Obtener claves expiradas
- Evicción por LRU
- Actualización del TTL al usar una clave


Resultado esperado
Una caché que:
- Mantiene solo datos válidos
- Elimina correctamente por tiempo
- Elimina correctamente por uso
- Respeta siempre la capacidad máxima

