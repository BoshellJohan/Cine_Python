import dearpygui.dearpygui as dpg
from Peliculas.Interfaz_Reservas import mostrar_interfaz_reserva_de_horario
from Funciones.funciones_generales_ventanas import close_popup_in_x_seconds


def clear_inputs():
    dpg.configure_item("nueva_pelicula_nombre", default_value="")
    dpg.configure_item("nueva_pelicula_descripcion", default_value="")
    dpg.configure_item("nueva_pelicula_duracion", default_value="")

def open_popup_cartelera(gestor_cine):
    print("Usuario en sesión:", gestor_cine.usuario_en_sesion)

    # Mostrar u ocultar el botón según si el administrador está activo
    if gestor_cine.administrador_activo:
        dpg.configure_item("button_agregar_pelicula_admin", show=True)
    else:
        dpg.configure_item("button_agregar_pelicula_admin", show=False)




def agregar_nueva_pelicula(sender, app_data, user_data):
    if dpg.does_item_exist("confirmacion_de_agregar_pelicula"):
        dpg.configure_item("confirmacion_de_agregar_pelicula", default_value="", show=False)

    gestor_cine = user_data
    nombre = dpg.get_value("nueva_pelicula_nombre")
    descripcion = dpg.get_value("nueva_pelicula_descripcion")
    duracion = dpg.get_value("nueva_pelicula_duracion")

    if nombre != ""  and descripcion != "" and duracion != "": #Inputs vacíos
        gestor_cine.agregar_pelicula_lista(nombre, descripcion, duracion)
        dpg.configure_item("confirmacion_de_agregar_pelicula", color=(0, 255, 0, 255), show=True, default_value="Pelicula agregada con exito a la cartelera")
    else:
        dpg.configure_item("confirmacion_de_agregar_pelicula", default_value=f"Los campos no se han rellenado correctamente.", show=True, color=(255, 0, 0, 255))




def ventana_agregar_nueva_pelicula(sender, app_data, user_data):
    gestor_cine = user_data

    # Comprobar si la ventana ya existe
    if dpg.does_item_exist(f"window_agregar_pelicula"):
        dpg.show_item(f"window_agregar_pelicula")
    else:
        # Crear una nueva ventana si no existe
        with dpg.window(label=f"Agregar nueva pelicula", tag=f"window_agregar_pelicula", width=500, height=400, modal=True, no_close=True):
            dpg.add_text("Ingrese la informacion de la nueva pelicula", tag="nueva_pelicula_texto")  # Texto de mensaje
            dpg.add_input_text(tag="nueva_pelicula_descripcion", label="Descripcion de la nueva pelicula")
            dpg.add_input_text(tag="nueva_pelicula_nombre", label="Nombre de la nueva pelicula")
            dpg.add_input_text(tag="nueva_pelicula_duracion", label="Duracion en minutos de la nueva pelicula")
            # dpg.add_input_text(tag="nueva_pelicula_", label="Nombre de la nueva pelicula")
            dpg.add_button(tag="button_agregar_nueva_pelicula", label="Agregar nueva pelicula a la cartelera", callback=agregar_nueva_pelicula, user_data=gestor_cine)
            dpg.add_text("",tag="confirmacion_de_agregar_pelicula", show=False)
            dpg.add_button(label="Cerrar", callback=cerrar_ventana, user_data="agregar_pelicula")


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


# Función para cerrar u ocultar la ventana de película
def cerrar_ventana(sender, app_data, user_data):
    info_ventana = user_data

    if dpg.does_item_exist(f"window_{info_ventana}"):
        dpg.hide_item(f"window_{info_ventana}")

    if info_ventana == "agregar_pelicula":
        clear_inputs()

# Función para mostrar los detalles de una película en una ventana hija
def mostrar_detalles_pelicula(sender, app_data, user_data):
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
                dpg.add_button(label=f"Hora: {horario['hora_inicio']}", tag=f'button_{pelicula.nombre}_{horario['hora_inicio']}', callback=mostrar_interfaz_reserva_de_horario, user_data=[gestor_cine, horario])
            # Botón para cerrar u ocultar la ventana
            dpg.add_button(label="Cerrar", callback=cerrar_ventana, user_data=pelicula.nombre)

