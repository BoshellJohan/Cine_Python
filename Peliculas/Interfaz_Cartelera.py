import dearpygui.dearpygui as dpg
from Peliculas.Interfaz_Reservas import mostrar_interfaz_reserva_de_horario
from Funciones.funciones_generales_ventanas import close_popup_in_x_seconds
from Peliculas.Interfaz_Administrador import ventana_agregar_nueva_pelicula, cerrar_ventana, ventana_agregar_nuevo_horario



def mostrar_cartelera(gestor_cine):
    lista_peliculas = gestor_cine.lista_peliculas

    # Crear un botón para cada película
    for pelicula in lista_peliculas:
        if pelicula is None:
            print("Error: La película es None.")
            continue
        if hasattr(pelicula, 'nombre') and pelicula.nombre:
            dpg.add_button(label=pelicula.nombre, callback=mostrar_detalles_pelicula, user_data=[gestor_cine, pelicula])
        else:
            print(f"Error: La película {pelicula} no tiene un nombre válido.")

    # Crear el botón para agregar películas (siempre existe, pero puede estar oculto)
    if not dpg.does_item_exist("button_agregar_pelicula_admin"):
        dpg.add_button(tag="button_agregar_pelicula_admin", label="Agregar pelicula", callback=ventana_agregar_nueva_pelicula, user_data=gestor_cine)

    #Crea el mensaje de error que indica al usuario que debe iniciar sesión para ver los detalles de las películas
    if not dpg.does_item_exist("mensaje_sesion_no_iniciada"):
        dpg.add_text("Nota: Debes iniciar sesión para ver los detalles y realizar reservas.", tag="mensaje_sesion_no_iniciada", color=(255,0,0,255))
    else:
        dpg.configure_item("mensaje_sesion_no_iniciada", show=True)






# Función para mostrar los detalles de una película en una ventana hija
def mostrar_detalles_pelicula(sender, app_data, user_data):
    gestor_cine = user_data[0]
    pelicula = user_data[1]

    if pelicula is None:
        print("Error: La película es None.")
        return

    if gestor_cine.usuario_en_sesion == True:
        # Comprobar si la ventana ya existe y eliminarla si está abierta
        if dpg.does_item_exist(f"window_{pelicula.nombre}"):
            dpg.delete_item(f"window_{pelicula.nombre}")

        # Crear una nueva ventana cada vez que se abre
        with dpg.window(label=f"Detalles de {pelicula.nombre}", tag=f"window_{pelicula.nombre}", width=400, height=300, modal=True, no_close=True):
            dpg.add_text(f"Descripción: {pelicula.descripcion}")
            dpg.add_text(f"Duración: {pelicula.duracion}")
            dpg.add_text("Horarios:")

            # Agregar los botones de horarios (si hay horarios)
            for horario in pelicula.horarios:
                dpg.add_button(label=f"Hora: {horario['hora_inicio']}", tag=f'button_{pelicula.nombre}_{horario["hora_inicio"]}', callback=mostrar_interfaz_reserva_de_horario, user_data=[gestor_cine, horario, pelicula.nombre])

            # Botón para cerrar la ventana y destruirla
            dpg.add_button(label="Cerrar", callback=cerrar_ventana, user_data=f"window_{pelicula.nombre}")

            # Crear el botón para agregar horarios a la película (solo si el administrador está activo)
            if not dpg.does_item_exist(f"button_agregar_horarios_{pelicula.nombre}_admin"):
                dpg.add_button(tag=f"button_agregar_horarios_{pelicula.nombre}_admin", label="Agregar horario", callback=ventana_agregar_nuevo_horario, user_data=[gestor_cine, pelicula], show=False)
                if gestor_cine.administrador_activo == True:
                    dpg.configure_item(f"button_agregar_horarios_{pelicula.nombre}_admin", show=True)

    else:
        dpg.configure_item("mensaje_sesion_no_iniciada", show=True)


