import dearpygui.dearpygui as dpg

# Función para crear la cartelera de películas
def mostrar_cartelera(lista_peliculas):
    for pelicula in lista_peliculas:
        if pelicula is None:
            print("Error: La película es None.")
            continue
        if hasattr(pelicula, 'nombre') and pelicula.nombre:
            # Crear un botón para cada película
            dpg.add_button(label=pelicula.nombre, callback=mostrar_detalles, user_data=pelicula)
        else:
            print(f"Error: La película {pelicula} no tiene un nombre válido.")

# Función para cerrar u ocultar la ventana de película
def cerrar_ventana_pelicula(sender, app_data, user_data):
    pelicula = user_data
    if dpg.does_item_exist(f"window_{pelicula.nombre}"):
        dpg.hide_item(f"window_{pelicula.nombre}")

# Función para mostrar los detalles de una película en una ventana hija
def mostrar_detalles(sender, app_data, user_data):
    pelicula = user_data
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
                dpg.add_text(f"- Sala {horario['sala']}, Hora: {horario['hora_inicio']}")
            # Botón para cerrar u ocultar la ventana
            dpg.add_button(label="Cerrar", callback=cerrar_ventana_pelicula, user_data=pelicula)
