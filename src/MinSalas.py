def minimoSalasReuniones(reuniones):
    # Lista donde guardaremos todos los eventos (inicio y fin de reuniones)
    eventos = []

     # Recorremos cada reunión
    for horaInicio, horaFin in reuniones:
        # Añadimos el evento de inicio (+1) y fin (-1)
        eventos.append((horaInicio, 1))  
        eventos.append((horaFin, -1)) 

    # Ordenamos los eventos por hora
    # Si dos eventos tienen la misma hora, el evento de fin (-1) debe ir antes que el de inicio (+1)    
    eventos.sort(key=lambda x: (x[0], x[1]))

    reuActivas = 0  
    maxReuniones = 0

    # Recorremos los eventos en orden de tiempo
    for _, cambio in eventos:
        reuActivas += cambio  # Actualizamos el número de reuniones activas

        # Guardamos el máximo número de reuniones activas en cualquier momento
        if reuActivas > maxReuniones:
           maxReuniones = reuActivas

    return maxReuniones

if __name__ == "__main__":
    # Ejemplos de uso
    reuniones = [(9, 10), (10, 11), (9, 11)]
    resultado = minimoSalasReuniones(reuniones)
    print(f"Reuniones: {reuniones}")
    print(f"Salas necesarias: {resultado}")

