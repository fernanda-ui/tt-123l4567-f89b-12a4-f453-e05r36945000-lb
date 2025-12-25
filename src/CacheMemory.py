import time


class CacheInMemory:
    """
    Caché en memoria con soporte para TTL (Time To Live) y LRU (Least Recently Used).
    
    TTL: Las entradas expiran después de un tiempo definido.
    LRU: Cuando la caché está llena, se elimina la entrada menos recientemente usada.
    """
    
    def __init__(self, capacity: int, DefaultTtlSeconds: int):
        """
        Inicializa la caché con capacidad y TTL por defecto.
        
        Args:
            capacity: Número máximo de entradas en la caché
            DefaultTtlSeconds: Tiempo de vida por defecto en segundos
        """
        self.capacity = capacity
        self.DefaultTtlSeconds = DefaultTtlSeconds
        
        # Diccionario principal: key -> {value, expiration_time, last_used}
        self.data = {}
        
        # Estadísticas (BONUS)
        self.stats_calls = 0  # Total de llamadas get/set
        self.stats_ttl_expired = 0  # Claves eliminadas por TTL
        self.stats_lru_evicted = 0  # Claves expulsadas por LRU

    def current_time(self):
        """Retorna el timestamp actual en segundos."""
        return time.time()

    def remove_expired(self):
        """
        Elimina todas las entradas que han expirado (TTL).
        Incrementa el contador de claves expiradas por TTL.
        """
        now = self.current_time()
        expired_keys = [
            key for key, entry in self.data.items()
            if entry["expiration_time"] < now
        ]

        # Incrementar contador de estadísticas
        self.stats_ttl_expired += len(expired_keys)
        
        for key in expired_keys:
            del self.data[key]

    def remove_lru(self):
        """
        Elimina la entrada menos recientemente usada (LRU).
        Se ejecuta cuando la caché alcanza su capacidad máxima.
        Incrementa el contador de claves expulsadas por LRU.
        """
        # Buscar la clave con el last_used más antiguo
        lru_key = min(
            self.data,
            key=lambda k: self.data[k]["last_used"]
        )
        
        # Incrementar contador de estadísticas
        self.stats_lru_evicted += 1
        
        del self.data[lru_key]

    def set(self, key: str, value: str):
        """
        Agrega una nueva clave o actualiza una existente en la caché.
        
        Comportamiento:
        - Si la clave existe: actualiza valor, TTL y last_used
        - Si es nueva y hay espacio: la agrega
        - Si es nueva y no hay espacio: expulsa la menos usada (LRU) y agrega
        - Siempre elimina entradas expiradas antes de operar
        
        Args:
            key: Clave a agregar o actualizar
            value: Valor asociado a la clave
        """
        now = self.current_time()
        
        # Incrementar contador de llamadas (estadísticas)
        self.stats_calls += 1

        # Limpiar entradas expiradas antes de verificar capacidad
        self.remove_expired()

        if key in self.data:
            # Actualizar entrada existente
            # Requisito: "Set cuenta como uso y renueva el TTL"
            self.data[key]["value"] = value
            self.data[key]["expiration_time"] = now + self.DefaultTtlSeconds
            self.data[key]["last_used"] = now
            return

        # Verificar si se necesita espacio (expulsión LRU)
        if len(self.data) >= self.capacity:
            self.remove_lru()

        # Agregar nueva entrada
        self.data[key] = {
            "value": value,
            "expiration_time": now + self.DefaultTtlSeconds,
            "last_used": now
        }

    def get(self, key: str):
        """
        Obtiene el valor de una clave de la caché.
        
        Comportamiento:
        - Si la clave no existe: retorna None
        - Si la clave expiró: la elimina y retorna None
        - Si la clave es válida: renueva su TTL, actualiza last_used y retorna el valor
        
        Args:
            key: Clave a consultar
            
        Returns:
            El valor asociado a la clave o None si no existe/expiró
        """
        now = self.current_time()
        
        # Incrementar contador de llamadas (estadísticas)
        self.stats_calls += 1

        # Verificar si la clave existe
        if key not in self.data:
            return None

        # Verificar si la clave expiró (TTL)
        if self.data[key]["expiration_time"] < now:
            # Eliminar clave expirada
            self.stats_ttl_expired += 1
            del self.data[key]
            return None

        # Requisito: "Get cuenta como uso y renueva el TTL"
        self.data[key]["expiration_time"] = now + self.DefaultTtlSeconds
        self.data[key]["last_used"] = now

        return self.data[key]["value"]

    def delete(self, key: str) -> bool:
        """
        Elimina una clave de la caché.
        
        Args:
            key: Clave a eliminar
            
        Returns:
            True si la clave existía y fue eliminada, False en caso contrario
        """
        if key in self.data:
            del self.data[key]
            return True
        return False

    def keys_and_values(self):
        """
        Retorna todas las claves y valores válidos (no expirados) de la caché.
        
        Limpia automáticamente las entradas expiradas antes de retornar.
        
        Returns:
            Lista de tuplas (key, value) con las entradas válidas
        """
        # Limpiar entradas expiradas antes de listar
        self.remove_expired()
        
        return [(key, entry["value"]) for key, entry in self.data.items()]
    
    def stats(self):
        """
        Retorna estadísticas de uso de la caché (BONUS).
        
        Returns:
            Diccionario con estadísticas:
            - total_calls: Número total de llamadas get/set
            - total_keys: Número actual de claves en la caché
            - ttl_expired: Claves eliminadas por TTL
            - lru_evicted: Claves expulsadas por LRU
        """
        # Limpiar expirados antes de contar claves actuales
        self.remove_expired()
        
        return {
            "total_calls": self.stats_calls,
            "total_keys": len(self.data),
            "ttl_expired": self.stats_ttl_expired,
            "lru_evicted": self.stats_lru_evicted
        }
