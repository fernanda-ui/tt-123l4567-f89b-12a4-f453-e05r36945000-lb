import time
from CacheMemory import CacheInMemory


def test_agregar_entradas_nuevas():
    """Tests para agregar entradas nuevas a la caché"""
    
    cache = CacheInMemory(capacity=3, DefaultTtlSeconds=10)
    
    # Agregar primera entrada
    cache.set("user1", "Alice")
    assert cache.get("user1") == "Alice", "Debe retornar el valor agregado"
    
    # Agregar segunda entrada
    cache.set("user2", "Bob")
    assert cache.get("user2") == "Bob", "Debe retornar el segundo valor"
    
    # Agregar tercera entrada (límite de capacidad)
    cache.set("user3", "Charlie")
    assert cache.get("user3") == "Charlie", "Debe retornar el tercer valor"
    
    # Verificar que todas existen
    keys_values = cache.keys_and_values()
    assert len(keys_values) == 3, "Debe haber 3 entradas"


def test_actualizar_entradas_existentes():
    """Tests para actualizar entradas que ya existen"""
    
    cache = CacheInMemory(capacity=3, DefaultTtlSeconds=10)
    
    # Agregar entrada inicial
    cache.set("config", "value1")
    assert cache.get("config") == "value1", "Valor inicial debe ser value1"
    
    # Actualizar la misma clave
    cache.set("config", "value2")
    assert cache.get("config") == "value2", "Valor debe actualizarse a value2"
    
    # Actualizar nuevamente
    cache.set("config", "value3")
    assert cache.get("config") == "value3", "Valor debe actualizarse a value3"
    
    # Verificar que solo existe una entrada
    keys_values = cache.keys_and_values()
    assert len(keys_values) == 1, "Solo debe haber 1 entrada"


def test_eliminar_entradas():
    """Tests para eliminar entradas de la caché"""
    
    cache = CacheInMemory(capacity=3, DefaultTtlSeconds=10)
    
    # Agregar entradas
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    
    # Eliminar una entrada existente
    result = cache.delete("key2")
    assert result == True, "Delete debe retornar True para clave existente"
    assert cache.get("key2") == None, "La clave eliminada no debe existir"
    
    # Verificar que las demás siguen existiendo
    assert cache.get("key1") == "value1", "key1 debe seguir existiendo"
    assert cache.get("key3") == "value3", "key3 debe seguir existiendo"
    
    # Intentar eliminar una entrada que no existe
    result = cache.delete("key_inexistente")
    assert result == False, "Delete debe retornar False para clave inexistente"
    
    # Eliminar todas
    cache.delete("key1")
    cache.delete("key3")
    keys_values = cache.keys_and_values()
    assert len(keys_values) == 0, "La caché debe estar vacía"


def test_leer_entradas_validas():
    """Tests para leer entradas válidas de la caché"""
    
    cache = CacheInMemory(capacity=5, DefaultTtlSeconds=10)
    
    # Agregar múltiples entradas
    cache.set("name", "John")
    cache.set("age", "30")
    cache.set("city", "Madrid")
    
    # Leer todas las entradas
    assert cache.get("name") == "John", "Debe retornar el valor correcto"
    assert cache.get("age") == "30", "Debe retornar el valor correcto"
    assert cache.get("city") == "Madrid", "Debe retornar el valor correcto"
    
    # Leer nuevamente (verificar que no se eliminan al leer)
    assert cache.get("name") == "John", "Debe retornar el valor tras múltiples lecturas"


def test_leer_entradas_inexistentes():
    """Tests para leer entradas que no existen"""
    
    cache = CacheInMemory(capacity=3, DefaultTtlSeconds=10)
    
    # Intentar leer de caché vacía
    result = cache.get("nonexistent")
    assert result == None, "Debe retornar None para clave inexistente"
    
    # Agregar una entrada y buscar otra diferente
    cache.set("existing", "value")
    result = cache.get("notexisting")
    assert result == None, "Debe retornar None para clave no agregada"
    
    # Verificar que la existente sigue disponible
    assert cache.get("existing") == "value", "La clave existente no debe verse afectada"


def test_leer_entradas_expiradas():
    """Tests para leer entradas que han expirado por TTL"""
    
    # Crear caché con TTL muy corto (2 segundos)
    cache = CacheInMemory(capacity=3, DefaultTtlSeconds=2)
    
    # Agregar entrada
    cache.set("temp_key", "temp_value")
    
    # Verificar que existe inmediatamente
    assert cache.get("temp_key") == "temp_value", "Debe existir recién agregada"
    
    # Esperar a que expire (2 segundos + margen)
    time.sleep(2.5)
    
    # Intentar leer entrada expirada
    result = cache.get("temp_key")
    assert result == None, "Debe retornar None para entrada expirada"
    
    # Verificar que fue eliminada
    keys_values = cache.keys_and_values()
    assert len(keys_values) == 0, "La entrada expirada debe ser eliminada"


def test_listar_todas_las_entradas():
    """Tests para listar todas las entradas válidas"""
    
    cache = CacheInMemory(capacity=5, DefaultTtlSeconds=10)
    
    # Caché vacía
    keys_values = cache.keys_and_values()
    assert keys_values == [], "Caché vacía debe retornar lista vacía"
    
    # Agregar múltiples entradas
    cache.set("a", "1")
    cache.set("b", "2")
    cache.set("c", "3")
    
    # Listar todas
    keys_values = cache.keys_and_values()
    assert len(keys_values) == 3, "Debe retornar 3 entradas"
    
    # Verificar que son tuplas (key, value)
    keys_dict = dict(keys_values)
    assert keys_dict["a"] == "1", "Debe contener el par correcto"
    assert keys_dict["b"] == "2", "Debe contener el par correcto"
    assert keys_dict["c"] == "3", "Debe contener el par correcto"


def test_expulsion_por_lru():
    """Tests para validar expulsión por LRU al superar capacidad"""
    
    # Caché con capacidad de 3 entradas
    cache = CacheInMemory(capacity=3, DefaultTtlSeconds=10)
    
    # Llenar la caché a capacidad máxima
    cache.set("key1", "value1")
    time.sleep(0.1)  # Pequeña pausa para diferenciar timestamps
    cache.set("key2", "value2")
    time.sleep(0.1)
    cache.set("key3", "value3")
    
    # Verificar que están todas
    assert cache.get("key1") == "value1"
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"
    
    # Agregar una cuarta entrada (debe expulsar la menos usada)
    time.sleep(0.1)
    cache.set("key4", "value4")
    
    # key1 debería haber sido expulsada (menos recientemente usada)
    # porque key2 y key3 fueron consultadas después
    keys_values = cache.keys_and_values()
    assert len(keys_values) == 3, "Debe mantener capacidad de 3"
    
    # Verificar que key4 existe
    assert cache.get("key4") == "value4", "La nueva entrada debe existir"


def test_expulsion_lru_con_uso_intermedio():
    """Test más específico de LRU con uso intermedio"""
    
    cache = CacheInMemory(capacity=3, DefaultTtlSeconds=10)
    
    # Agregar 3 entradas
    cache.set("a", "1")
    time.sleep(0.1)
    cache.set("b", "2")
    time.sleep(0.1)
    cache.set("c", "3")
    time.sleep(0.1)
    
    # Usar "a" para actualizar su last_used
    cache.get("a")
    time.sleep(0.1)
    
    # Usar "c" para actualizar su last_used
    cache.get("c")
    time.sleep(0.1)
    
    # Ahora "b" es la menos recientemente usada
    # Agregar nueva entrada debe expulsar "b"
    cache.set("d", "4")
    
    # Verificar que "b" fue expulsada
    assert cache.get("b") == None, "b debe haber sido expulsada (LRU)"
    
    # Verificar que las demás existen
    assert cache.get("a") == "1", "a debe existir (fue usada)"
    assert cache.get("c") == "3", "c debe existir (fue usada)"
    assert cache.get("d") == "4", "d debe existir (recién agregada)"


def test_actualizacion_ttl_al_usar():
    """Test para confirmar que el TTL se renueva al usar una clave"""
    
    # Caché con TTL de 3 segundos
    cache = CacheInMemory(capacity=3, DefaultTtlSeconds=3)
    
    # Agregar entrada
    cache.set("renew_key", "renew_value")
    
    # Esperar casi el tiempo de expiración (2 segundos)
    time.sleep(2)
    
    # Usar la clave (debe renovar su TTL)
    result = cache.get("renew_key")
    assert result == "renew_value", "Debe existir antes de expirar"
    
    # Esperar otros 2 segundos (total 4, pero TTL se renovó)
    time.sleep(2)
    
    # La clave aún debe existir porque se renovó su TTL
    result = cache.get("renew_key")
    assert result == "renew_value", "Debe existir porque TTL se renovó al usarla"
    
    # Esperar que expire definitivamente (3 segundos sin uso)
    time.sleep(3.5)
    
    # Ahora sí debe haber expirado
    result = cache.get("renew_key")
    assert result == None, "Debe haber expirado tras 3 segundos sin uso"


def test_actualizacion_ttl_con_set():
    """Test para verificar que set() también renueva el TTL"""
    
    cache = CacheInMemory(capacity=3, DefaultTtlSeconds=3)
    
    # Agregar entrada
    cache.set("update_key", "value1")
    
    # Esperar casi el tiempo de expiración
    time.sleep(2)
    
    # Actualizar la entrada (debe renovar TTL)
    cache.set("update_key", "value2")
    
    # Esperar otros 2 segundos
    time.sleep(2)
    
    # Debe seguir existiendo (TTL renovado)
    result = cache.get("update_key")
    assert result == "value2", "Debe existir con valor actualizado"


def test_estadisticas_basicas():
    """Tests para el método stats() (BONUS)"""
    
    cache = CacheInMemory(capacity=3, DefaultTtlSeconds=10)
    
    # Estadísticas iniciales
    stats = cache.stats()
    assert stats["total_calls"] == 0, "No debe haber llamadas inicialmente"
    assert stats["total_keys"] == 0, "No debe haber claves inicialmente"
    assert stats["ttl_expired"] == 0, "No debe haber expiraciones inicialmente"
    assert stats["lru_evicted"] == 0, "No debe haber expulsiones inicialmente"
    
    # Realizar operaciones
    cache.set("key1", "value1")  # 1 llamada
    cache.set("key2", "value2")  # 2 llamadas
    cache.get("key1")             # 3 llamadas
    
    stats = cache.stats()
    assert stats["total_calls"] == 3, "Debe contar 3 llamadas (2 set + 1 get)"
    assert stats["total_keys"] == 2, "Debe haber 2 claves"


def test_estadisticas_ttl_expired():
    """Test para contador de claves expiradas por TTL"""
    
    cache = CacheInMemory(capacity=5, DefaultTtlSeconds=1)
    
    # Agregar entradas
    cache.set("temp1", "value1")
    cache.set("temp2", "value2")
    
    # Esperar expiración
    time.sleep(1.5)
    
    # Intentar leer (detecta expiración)
    cache.get("temp1")
    
    # Verificar estadísticas
    stats = cache.stats()
    assert stats["ttl_expired"] >= 1, "Debe contar al menos 1 expiración"


def test_estadisticas_lru_evicted():
    """Test para contador de claves expulsadas por LRU"""
    
    cache = CacheInMemory(capacity=2, DefaultTtlSeconds=10)
    
    # Llenar capacidad
    cache.set("a", "1")
    cache.set("b", "2")
    
    # Forzar expulsión LRU
    cache.set("c", "3")
    
    # Verificar estadísticas
    stats = cache.stats()
    assert stats["lru_evicted"] == 1, "Debe contar 1 expulsión LRU"
    
    # Otra expulsión
    cache.set("d", "4")
    
    stats = cache.stats()
    assert stats["lru_evicted"] == 2, "Debe contar 2 expulsiones LRU"


def test_casos_borde():
    """Tests de casos borde y extremos"""
    
    # Caché con capacidad mínima
    cache = CacheInMemory(capacity=1, DefaultTtlSeconds=10)
    
    cache.set("only", "value")
    assert cache.get("only") == "value"
    
    # Agregar otra debe expulsar la anterior
    cache.set("second", "value2")
    assert cache.get("only") == None, "Primera entrada debe ser expulsada"
    assert cache.get("second") == "value2", "Segunda entrada debe existir"
    
    # TTL de 0 segundos (expira inmediatamente)
    cache_zero = CacheInMemory(capacity=3, DefaultTtlSeconds=0)
    cache_zero.set("instant", "value")
    time.sleep(0.1)
    result = cache_zero.get("instant")
    assert result == None, "Entrada con TTL=0 debe expirar inmediatamente"


def test_operaciones_mixtas():
    """Test con operaciones mixtas complejas"""
    
    cache = CacheInMemory(capacity=3, DefaultTtlSeconds=5)
    
    # Operaciones variadas
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    assert cache.get("key1") == "value1"
    
    cache.delete("key2")
    assert cache.get("key2") == None
    
    cache.set("key3", "value3")
    cache.set("key1", "updated_value1")  # Actualizar
    
    assert cache.get("key1") == "updated_value1"
    
    keys_values = cache.keys_and_values()
    assert len(keys_values) == 2  # key1 y key3


if __name__ == "__main__":
    print("Ejecutando tests de CacheMemory...")
    
    print("\n=== Tests de operaciones básicas ===")
    test_agregar_entradas_nuevas()
    print("✓ Test agregar entradas nuevas pasó")
    
    test_actualizar_entradas_existentes()
    print("✓ Test actualizar entradas existentes pasó")
    
    test_eliminar_entradas()
    print("✓ Test eliminar entradas pasó")
    
    test_leer_entradas_validas()
    print("✓ Test leer entradas válidas pasó")
    
    test_leer_entradas_inexistentes()
    print("✓ Test leer entradas inexistentes pasó")
    
    print("\n=== Tests de TTL ===")
    test_leer_entradas_expiradas()
    print("✓ Test leer entradas expiradas pasó")
    
    test_actualizacion_ttl_al_usar()
    print("✓ Test actualización TTL al usar pasó")
    
    test_actualizacion_ttl_con_set()
    print("✓ Test actualización TTL con set pasó")
    
    print("\n=== Tests de LRU ===")
    test_expulsion_por_lru()
    print("✓ Test expulsión por LRU pasó")
    
    test_expulsion_lru_con_uso_intermedio()
    print("✓ Test expulsión LRU con uso intermedio pasó")
    
    print("\n=== Tests de listado ===")
    test_listar_todas_las_entradas()
    print("✓ Test listar todas las entradas pasó")
    
    print("\n=== Tests de estadísticas (BONUS) ===")
    test_estadisticas_basicas()
    print("✓ Test estadísticas básicas pasó")
    
    test_estadisticas_ttl_expired()
    print("✓ Test estadísticas TTL expired pasó")
    
    test_estadisticas_lru_evicted()
    print("✓ Test estadísticas LRU evicted pasó")
    
    print("\n=== Tests de casos borde ===")
    test_casos_borde()
    print("✓ Test casos borde pasó")
    
    test_operaciones_mixtas()
    print("✓ Test operaciones mixtas pasó")
    
    print("\n" + "="*50)
    print("✓ TODOS LOS TESTS PASARON EXITOSAMENTE (16 tests)")
    print("="*50)
