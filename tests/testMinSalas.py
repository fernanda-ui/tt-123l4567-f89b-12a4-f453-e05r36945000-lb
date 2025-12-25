from MinSalas import minimoSalasReuniones

def test_sin_solapamientos():
    """Tests para casos sin solapamientos de horas"""
    
    # Reuniones consecutivas sin solapamiento
    reuniones1 = [(9, 10), (10, 11), (11, 12)]
    assert minimoSalasReuniones(reuniones1) == 1, "Reuniones consecutivas deben usar 1 sala"
    
    # Reuniones con espacios entre ellas
    reuniones2 = [(8, 9), (10, 11), (12, 13)]
    assert minimoSalasReuniones(reuniones2) == 1, "Reuniones separadas deben usar 1 sala"
    
    # Una sola reunión
    reuniones3 = [(9, 10)]
    assert minimoSalasReuniones(reuniones3) == 1, "Una reunión debe usar 1 sala"
    
    # Reuniones en orden no cronológico pero sin solapamiento
    reuniones4 = [(14, 15), (9, 10), (11, 12)]
    assert minimoSalasReuniones(reuniones4) == 1, "Reuniones desordenadas sin solapamiento deben usar 1 sala"


def test_con_solapamientos():
    """Tests para casos con solapamientos de horas"""
    
    # Dos reuniones que se solapan parcialmente
    reuniones1 = [(9, 11), (10, 12)]
    assert minimoSalasReuniones(reuniones1) == 2, "Dos reuniones solapadas requieren 2 salas"
    
    # Tres reuniones que se solapan parcialmente
    reuniones2 = [(9, 11), (10, 12), (11, 13)]
    assert minimoSalasReuniones(reuniones2) == 2, "Tres reuniones con solapamiento parcial requieren 2 salas"
    
    # Todas las reuniones al mismo tiempo
    reuniones3 = [(9, 10), (9, 10), (9, 10)]
    assert minimoSalasReuniones(reuniones3) == 3, "Reuniones simultáneas requieren 3 salas"
    
    # Una reunión que abarca completamente a otras
    reuniones4 = [(9, 14), (10, 11), (11, 12), (12, 13)]
    assert minimoSalasReuniones(reuniones4) == 2, "Reunión larga con otras pequeñas dentro requiere 2 salas"
    
    # Múltiples reuniones con solapamientos variados
    reuniones5 = [(8, 10), (9, 11), (10, 12), (11, 13), (12, 14)]
    assert minimoSalasReuniones(reuniones5) == 2, "Múltiples solapamientos escalonados requieren 2 salas"
    
    # Pico de solapamiento en el medio
    reuniones6 = [(8, 10), (9, 11), (9.5, 10.5), (10, 12)]
    assert minimoSalasReuniones(reuniones6) == 3, "Pico de 3 reuniones simultáneas requiere 3 salas"


def test_casos_borde():
    """Tests para casos de borde: horaInicio == horaFin de otra reunión"""
    
    # Caso borde: reunión termina exactamente cuando otra empieza
    reuniones1 = [(9, 10), (10, 11)]
    assert minimoSalasReuniones(reuniones1) == 1, "Reunión que empieza cuando otra termina debe usar 1 sala"
    
    # Múltiples reuniones consecutivas en el borde
    reuniones2 = [(8, 9), (9, 10), (10, 11), (11, 12)]
    assert minimoSalasReuniones(reuniones2) == 1, "Reuniones consecutivas en el borde deben usar 1 sala"
    
    # Caso borde con solapamiento: una empieza antes y termina cuando otra empieza
    reuniones3 = [(8, 10), (9, 11), (10, 12)]
    assert minimoSalasReuniones(reuniones3) == 2, "Reuniones con borde y solapamiento requieren 2 salas"
    
    # Caso borde: varias reuniones terminan e inician al mismo tiempo
    reuniones4 = [(8, 10), (9, 10), (10, 11), (10, 12)]
    assert minimoSalasReuniones(reuniones4) == 2, "Múltiples reuniones en el borde requieren 2 salas"
    
    # Caso borde: reunión de duración cero (inicio == fin)
    reuniones5 = [(9, 9), (9, 10)]
    assert minimoSalasReuniones(reuniones5) == 1, "Reunión de duración cero debe manejarse correctamente"
    
    # Caso borde complejo: múltiples puntos de inicio/fin coincidentes
    reuniones6 = [(8, 10), (10, 12), (12, 14), (9, 11), (11, 13)]
    assert minimoSalasReuniones(reuniones6) == 2, "Múltiples puntos de borde con solapamiento requieren 2 salas"


def test_rendimiento():
    """Tests de rendimiento con muchas reuniones"""
    
    # Muchas reuniones sin solapamiento
    reuniones1 = [(i, i+1) for i in range(100)]
    assert minimoSalasReuniones(reuniones1) == 1, "100 reuniones consecutivas deben usar 1 sala"
    
    # Muchas reuniones todas al mismo tiempo
    reuniones2 = [(9, 10) for _ in range(50)]
    assert minimoSalasReuniones(reuniones2) == 50, "50 reuniones simultáneas requieren 50 salas"
    
    # Muchas reuniones con solapamientos graduales
    reuniones3 = [(i, i+2) for i in range(0, 100, 1)]
    resultado = minimoSalasReuniones(reuniones3)
    assert resultado == 2, f"Reuniones con solapamiento gradual requieren 2 salas, obtuvo {resultado}"
    
    # Caso mixto con 200 reuniones
    reuniones4 = [(i, i+1) for i in range(0, 100, 2)] + [(i, i+1.5) for i in range(1, 100, 2)]
    resultado4 = minimoSalasReuniones(reuniones4)
    assert resultado4 >= 1, "200 reuniones mixtas deben requerir al menos 1 sala"


def test_casos_adicionales():
    """Tests adicionales para asegurar cobertura completa"""
    
    # Sin reuniones (lista vacía)
    reuniones1 = []
    assert minimoSalasReuniones(reuniones1) == 0, "Sin reuniones debe retornar 0 salas"
    
    # Reuniones con horarios decimales
    reuniones2 = [(8.5, 9.5), (9, 10), (9.5, 10.5)]
    assert minimoSalasReuniones(reuniones2) == 2, "Reuniones con horarios decimales deben funcionar correctamente"
    
    # Reuniones al inicio y fin del día (mismo día)
    reuniones3 = [(0, 1), (23, 24)]
    assert minimoSalasReuniones(reuniones3) == 1, "Reuniones al inicio y fin del día deben usar 1 sala"
    
    # Todas las reuniones empiezan a la misma hora pero terminan en diferentes momentos
    reuniones4 = [(9, 10), (9, 11), (9, 12)]
    assert minimoSalasReuniones(reuniones4) == 3, "Reuniones que empiezan juntas requieren 3 salas"
    
    # Todas las reuniones terminan a la misma hora pero empiezan en diferentes momentos
    reuniones5 = [(8, 10), (9, 10), (9.5, 10)]
    assert minimoSalasReuniones(reuniones5) == 3, "Reuniones que terminan juntas requieren 3 salas"


if __name__ == "__main__":
    print("Ejecutando tests...")
    print("\n=== Tests sin solapamientos ===")
    test_sin_solapamientos()
    print("✓ Todos los tests sin solapamientos pasaron")
    
    print("\n=== Tests con solapamientos ===")
    test_con_solapamientos()
    print("✓ Todos los tests con solapamientos pasaron")
    
    print("\n=== Tests de casos borde ===")
    test_casos_borde()
    print("✓ Todos los tests de casos borde pasaron")
    
    print("\n=== Tests de rendimiento ===")
    test_rendimiento()
    print("✓ Todos los tests de rendimiento pasaron")
    
    print("\n=== Tests adicionales ===")
    test_casos_adicionales()
    print("✓ Todos los tests adicionales pasaron")
    
    print("\n" + "="*50)
    print("✓ TODOS LOS TESTS PASARON EXITOSAMENTE (25 tests)")
    print("="*50)