import dearpygui.dearpygui as dpg
from Reservas_Salas.clases_reservas import Sala

# Función para crear la cartelera de películas
def mostrar_cartelera(gestor_cine):
    lista_peliculas = gestor_cine.lista_peliculas

    for pelicula in lista_peliculas:
        if pelicula is None:
            print("Error: La película es None.")
            continue
        if hasattr(pelicula, 'nombre') and pelicula.nombre:
            # Crear un botón para cada película
            dpg.add_button(label=pelicula.nombre, callback=mostrar_detalles, user_data=[gestor_cine, pelicula])
        else:
            print(f"Error: La película {pelicula} no tiene un nombre válido.")

# Función para cerrar u ocultar la ventana de película
def cerrar_ventana_pelicula(sender, app_data, user_data):
    pelicula = user_data
    if dpg.does_item_exist(f"window_{pelicula.nombre}"):
        dpg.hide_item(f"window_{pelicula.nombre}")

# Función para mostrar los detalles de una película en una ventana hija
def mostrar_detalles(sender, app_data, user_data):
    gestor_cine = user_data[0]
    pelicula = user_data[1]

    if pelicula is None:
        print("Error: La película es None.")
        return

    # Comprobar si la ventana ya existe
    if dpg.does_item_exist(f"window_{pelicula.nombre}"):
        dpg.show_item(f"window_{pelicula.nombre}")
    else:
        # Crear una nueva ventana si no existe
        with dpg.window(label=f"Detalles de {pelicula.nombre}", tag=f"window_{pelicula.nombre}", width=400, height=300, modal=True, no_close=True):
            dpg.add_text(f"Descripción: {pelicula.descripcion}")
            dpg.add_text(f"Duración: {pelicula.duracion}")
            dpg.add_text("Horarios:")
            for horario in pelicula.horarios:
                # dpg.add_text(f"- Sala {horario['sala']}, Hora: {horario['hora_inicio']}")
                dpg.add_button(label=f"Hora: {horario['hora_inicio']}", tag=f'button_{pelicula.nombre}_{horario['hora_inicio']}', callback=mostrar_interfaz_reserva_de_horario, user_data=[gestor_cine, horario])
            # Botón para cerrar u ocultar la ventana
            dpg.add_button(label="Cerrar", callback=cerrar_ventana_pelicula, user_data=pelicula)


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

