import dearpygui.dearpygui as dpg
from Peliculas.Interfaz_Reservas import mostrar_interfaz_reserva_de_horario
from Funciones.funciones_generales_ventanas import close_popup_in_x_seconds
from Administrador.Interfaz_Administrador import ventana_agregar_nueva_pelicula, cerrar_ventana, ventana_agregar_nuevo_horario
import math

def mostrar_cartelera(gestor_cine):
    # Tag del contenedor de la cartelera
    cartelera_tag = "cartelera_contenedor"

    # Si el contenedor ya existe, eliminarlo para actualizarlo
    if dpg.does_item_exist(cartelera_tag):
        dpg.delete_item(cartelera_tag)

    # Crear un contenedor para la cartelera
    with dpg.group(tag=cartelera_tag):
        lista_peliculas = gestor_cine.lista_peliculas
        peliculas_por_fila = 6  # Numero de peliculas por fila
        total_peliculas = len(lista_peliculas)

        # Dividir la lista en bloques de 4
        n = math.ceil(total_peliculas / peliculas_por_fila)  # Numero de filas necesarias

        for i in range(n):
            # Crear el grupo horizontal (fila)
            with dpg.group(horizontal=True):
                # Crear los botones para cada pelicula en la fila actual
                for j in range(peliculas_por_fila):
                    index = i * peliculas_por_fila + j  # Calcular el indice de la pelicula actual
                    if index >= total_peliculas:
                        break  # Salir si hemos alcanzado el final de la lista

                    pelicula = lista_peliculas[index]

                    if pelicula is None:
                        print("Error: La pelicula es None.")
                        continue

                    if hasattr(pelicula, 'nombre') and pelicula.nombre:
                        # Añadir un contenedor para cada pelicula (horizontal=False para alineacion vertical dentro de cada celda)
                        with dpg.group(horizontal=False):
                            # Añadir imagen de la pelicula (deberas tener un archivo de imagen)
                            dpg.add_image("texture_tag", width=240, height=150)  # Ajusta el tamaño de la imagen

                            # Añadir boton de la pelicula con un tamaño distinto al de la imagen
                            dpg.add_button(
                                label=pelicula.nombre,
                                callback=mostrar_detalles_pelicula,
                                user_data=[gestor_cine, pelicula],
                                width=240,
                                height=50  # Ajusta el tamaño del boton
                            )
                    else:
                        print(f"Error: La pelicula {pelicula} no tiene un nombre valido.")


        # Crear el boton para agregar peliculas (siempre existe, pero puede estar oculto)
        if not dpg.does_item_exist("button_agregar_pelicula_admin"):
            dpg.add_button(tag="button_agregar_pelicula_admin", label="Agregar pelicula", callback=ventana_agregar_nueva_pelicula, user_data=gestor_cine)

        # Crear el mensaje de error que indica al usuario que debe iniciar sesion para ver los detalles
        if not dpg.does_item_exist("mensaje_sesion_no_iniciada"):
            dpg.add_text("Nota: Debes iniciar sesion para ver los detalles y realizar reservas.", tag="mensaje_sesion_no_iniciada", color=(255, 0, 0, 255))
        else:
            dpg.configure_item("mensaje_sesion_no_iniciada", show=True)






# Funcion para mostrar los detalles de una pelicula en una ventana hija
def mostrar_detalles_pelicula(sender, app_data, user_data):
    gestor_cine = user_data[0]
    pelicula = user_data[1]

    if pelicula is None:
        print("Error: La pelicula es None.")
        return

    if gestor_cine.usuario_en_sesion == True:
        # Comprobar si la ventana ya existe y eliminarla si esta abierta
        if dpg.does_item_exist(f"window_{pelicula.nombre}"):
            dpg.delete_item(f"window_{pelicula.nombre}")

        # Crear una nueva ventana cada vez que se abre
        with dpg.window(label=f"Detalles de {pelicula.nombre}", tag=f"window_{pelicula.nombre}", width=450, height=350, modal=True, no_close=True, pos=(400, 0)):
            dpg.add_text(f"Nombre: {pelicula.nombre}")

            # Ajuste automatico de texto (word wrap) para la descripcion
            dpg.add_text(f"Descripcion: {pelicula.descripcion}", wrap=400)  # Ajustar al ancho de 400 pixeles

            dpg.add_text(f"Duracion: {pelicula.duracion} mins")
            dpg.add_text("\nHorarios:")

            if pelicula.horarios:
                # Agregar los botones de horarios (si hay horarios)
                for horario in pelicula.horarios:
                    dpg.add_button(label=f"Hora: {horario['hora_inicio']}", tag=f'button_{pelicula.nombre}_{horario["hora_inicio"]}', callback=mostrar_interfaz_reserva_de_horario, user_data=[gestor_cine, horario, pelicula.nombre])

            else:
                dpg.add_text("No hay horarios disponibles en este momento.")

            # Boton para cerrar la ventana y destruirla
            dpg.add_button(label="Cerrar", callback=cerrar_ventana, user_data=f"window_{pelicula.nombre}")

            # Espaciador para separar la cartelera
            dpg.add_spacer(height=20)

            # Crear el boton para agregar horarios a la pelicula (solo si el administrador esta activo)
            if not dpg.does_item_exist(f"button_agregar_horarios_{pelicula.nombre}_admin"):
                dpg.add_button(tag=f"button_agregar_horarios_{pelicula.nombre}_admin", label="Agregar horario", callback=ventana_agregar_nuevo_horario, user_data=[gestor_cine, pelicula], show=False)
                if gestor_cine.administrador_activo == True:
                    dpg.configure_item(f"button_agregar_horarios_{pelicula.nombre}_admin", show=True)

    else:
        dpg.configure_item("mensaje_sesion_no_iniciada", show=True)

