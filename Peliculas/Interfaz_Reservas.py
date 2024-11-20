from Reservas_Salas.clases_reservas import Sala


def mostrar_interfaz_reserva_de_horario(sender, app_data, user_data):
    gestor_cine = user_data[0]
    horario = user_data[1]
    num_sala_de_funcion = horario['sala']
    hora_de_funcion = horario['hora_inicio']

    sala_funcion = None

    for sala in gestor_cine.lista_salas:
        if sala.numero_sala == num_sala_de_funcion:
            sala_funcion = sala
            break

    print(f"Sala del horario: {num_sala_de_funcion}, Sala lógica: {sala.numero_sala}")
    if isinstance(sala_funcion, Sala):
        # Verificar si el horario existe en la sala

        if hora_de_funcion in sala.horarios:
            asientos_ocupados = sala.horarios[hora_de_funcion]["asientos_ocupados"]
            print(f"Asientos ocupados para la función de las {hora_de_funcion}: {asientos_ocupados}")
        else:
            print(f"No se encontró la hora de función '{hora_de_funcion}'.")

    else:
        print("Error encontrando la sala del horario.")

