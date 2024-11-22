import dearpygui.dearpygui as dpg
from Funciones.funciones_generales_ventanas import close_popup_in_x_seconds
import re


# Función para cerrar u ocultar la ventana de película
def cerrar_ventana(sender, app_data, user_data):
    info_ventana = user_data

    if dpg.does_item_exist(f"{info_ventana}"):
        dpg.hide_item(f"{info_ventana}")

    if info_ventana == "window_agregar_pelicula":
        clear_inputs()



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
        close_popup_in_x_seconds(3, "window_agregar_pelicula")
        dpg.hide_item("window_agregar_pelicula")
        clear_inputs()

        dpg.configure_item("mensaje_sesion_no_iniciada", default_value=f"La nueva pelicula '{nombre}' estara disponible en la cartelera al reiniciar el programa.", color=(0,255,0,255), show=True)
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
            dpg.add_button(label="Cerrar", callback=cerrar_ventana, user_data="window_agregar_pelicula")



def validar_hora(hora):
    # Expresión regular para validar el formato HH:MM
    patron_hora = r"^[0-2][0-9]:[0-5][0-9]$"

    # Comprobar si la hora coincide con el patrón
    if re.match(patron_hora, hora):
        return True
    else:
        return False


def agregar_nuevo_horario(sender, app_data, user_data):
    gestor_cine = user_data[0]
    pelicula = user_data[1]
    dpg.configure_item(f"mensaje_acerca_{pelicula.nombre}", default_value="", show=False)


    nuevo_horario = dpg.get_value(f"nuevo_horario_hora_{pelicula.nombre}")
    print(nuevo_horario)

    # Validar el formato de la hora
    if validar_hora(nuevo_horario):
        # Proceder con la lógica de agregar el nuevo horario
        print(f"Nuevo horario válido: {nuevo_horario}")
        #Se ha agregado el horario a la pelicula?
        if pelicula.agregar_horario(nuevo_horario, gestor_cine.lista_salas):
            dpg.configure_item(f"mensaje_acerca_{pelicula.nombre}", default_value=f"Horario agregado con exito a la pelicula '{pelicula.nombre}'.", show=True, color=(0,255,0,255))
            gestor_cine.guardar_peliculas_archivo()
            gestor_cine.guardar_salas_archivo()

            gestor_cine.cargar_peliculas_archivo()
            gestor_cine.cargar_salas_archivo()

            close_popup_in_x_seconds(2, f"window_agregar_horario_{pelicula.nombre}")
        else:
            dpg.configure_item(f"mensaje_acerca_{pelicula.nombre}", default_value=f"Ninguna sala esta disponible en ese horario para la pelicula '{pelicula.nombre}'.", show=True, color=(255,0,0,255))

    else:
        # Mostrar un mensaje de error si el formato no es válido
        dpg.configure_item(f"mensaje_acerca_{pelicula.nombre}", default_value="Formato de hora incorrecto. Debe ser XX:XX.", show=True, color=(255,0,0,255))


def ventana_agregar_nuevo_horario(sender, app_data, user_data):
    gestor_cine = user_data[0]
    pelicula = user_data[1]

    # Cerrar ventana de detalles de película si están abiertas
    ventana_info_tag = f"window_{pelicula.nombre}"
    if dpg.does_item_exist(ventana_info_tag):
        dpg.hide_item(ventana_info_tag)

    # Crear la ventana de agregar horario
    ventana_tag = f"window_agregar_horario_{pelicula.nombre}"
    if dpg.does_item_exist(ventana_tag):
        # Si la ventana ya existe, mostrarla
        dpg.delete_item(ventana_tag)

    # Si no existe, crearla
    with dpg.window(label=f"Agregar nuevo horario", tag=ventana_tag, width=800, height=200, modal=False, no_close=True, no_resize=True, no_move=True, pos=(300, 300)):
        dpg.add_text(f"Ingrese la informacion del nuevo horario para la pelicula '{pelicula.nombre}'", tag=f"nuevo_horario_texto_{pelicula.nombre}")
        dpg.add_input_text(tag=f"nuevo_horario_hora_{pelicula.nombre}", label="Ingrese el nuevo horario en el siguiente formato XX:XX -> ")
        dpg.add_button(tag=f"button_agregar_nuevo_horario_{pelicula.nombre}", label="Agregar nuevo horario para la pelicula", callback=agregar_nuevo_horario, user_data=[gestor_cine, pelicula])
        dpg.add_text("", tag=f"mensaje_acerca_{pelicula.nombre}", show=False)
        dpg.add_button(label="Cerrar", callback=cerrar_ventana, user_data=ventana_tag)
