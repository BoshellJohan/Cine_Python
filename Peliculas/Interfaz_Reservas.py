import dearpygui.dearpygui as dpg
from Reservas_Salas.clases_reservas import Sala
from Objetos_Diseño.temas import crear_temas
from Peliculas.Analisis_compra import comprobar_compra
from Funciones.funciones_generales_ventanas import cerrar_ventana_reservas_in_x_segundos


def mostrar_interfaz_reserva_de_horario(sender, app_data, user_data):
    # Resetear la lista de asientos elegidos
    gestor_cine = user_data[0]
    gestor_cine.lista_compra_asientos = []

    horario = user_data[1]
    nombre_pelicula = user_data[2]

    num_sala_de_funcion = horario['sala']
    hora_de_funcion = horario['hora_inicio']
    gestor_cine.cant_boletas = 0

    # Cerrar ventana de detalles de pelicula si esta abierta
    ventana_info_tag = f"window_{nombre_pelicula}"
    if dpg.does_item_exist(ventana_info_tag):
        dpg.hide_item(ventana_info_tag)

    # Buscar sala
    for sala in gestor_cine.lista_salas:
        if sala.numero_sala == num_sala_de_funcion:
            sala_funcion = sala
            break
    else:
        print("Error encontrando la sala del horario.")
        return

    # Calcular el tamaño de la ventana dinamicamente
    asiento_width = 45
    asiento_height = 45
    espacio_horizontal = 10
    espacio_vertical = 10

    ventana_width = sala_funcion.numeracion_maxima * (asiento_width + espacio_horizontal) + 50
    ventana_height = (ord(sala_funcion.letra_max) - ord('A') + 1) * (asiento_height + espacio_vertical) + 100

    ventana_tag = f"window_{num_sala_de_funcion}_{hora_de_funcion}"
    if dpg.does_item_exist(ventana_tag):
        dpg.delete_item(ventana_tag)

    with dpg.window(
        label=f"Reserva Pelicula - {nombre_pelicula}",
        tag=ventana_tag,
        width=ventana_width,
        height=ventana_height,
        modal=False,
        no_close=True,
        no_resize=True,
        no_move=True,
        pos=(300, 0)
    ):
        dpg.add_text(f"Reservas para la funcion de las {hora_de_funcion}. Pelicula: '{nombre_pelicula}'", color=(0, 0, 0, 255))
        # Verificar si el horario existe en la sala
        if hora_de_funcion in sala_funcion.horarios:
            asientos_ocupados = sala_funcion.horarios[hora_de_funcion]["asientos_ocupados"]
            interfaz_sillas(sala_funcion, asientos_ocupados, gestor_cine, ventana_tag)
            dpg.add_text(f"Precio: {gestor_cine.cant_boletas * gestor_cine.precio_boleta}, Boletas: {gestor_cine.cant_boletas}", tag=f"compra_info", color=(0, 0, 0, 255))
            dpg.add_button(label="Comprar boletas", callback=comprobar_compra, user_data=[gestor_cine, sala_funcion, hora_de_funcion, ventana_tag])
            dpg.add_text("", tag="Resultado_de_compra", show=False)
        else:
            print(f"No se encontro la hora de funcion '{hora_de_funcion}'.")

        dpg.add_button(label="Cerrar", callback=lambda: cerrar_ventana_reservas_in_x_segundos(0, ventana_tag, sala_funcion))


def interfaz_sillas(sala, asientos_ocupados, gestor_cine, ventana_tag):
    letra_max = sala.letra_max
    numeracion_maxima = sala.numeracion_maxima
    tema_disponible, tema_seleccionado, tema_ocupado = crear_temas()

    with dpg.group(parent=ventana_tag):
        for letra in range(ord('A'), ord(letra_max) + 1):
            # Grupo para una fila horizontal
            with dpg.group(horizontal=True):
                for numero in range(1, numeracion_maxima + 1):
                    asiento = f"{chr(letra)}{numero}"
                    if asiento in asientos_ocupados:
                        # Asiento ocupado
                        dpg.add_button(label=asiento, tag=f"{asiento}_{sala.numero_sala}", width=45, height=45)
                        dpg.bind_item_theme(f"{asiento}_{sala.numero_sala}", tema_ocupado)
                    else:
                        # Asiento disponible
                        obj_asiento = Asiento(asiento)
                        asiento_tag = f"{asiento}_{sala.numero_sala}"
                        dpg.add_button(
                            label=asiento,
                            tag=asiento_tag,
                            callback=agregar_asiento_carrito,
                            user_data=[obj_asiento, gestor_cine],
                            width=45,
                            height=45
                        )
                        dpg.bind_item_theme(asiento_tag, tema_disponible)




def agregar_asiento_carrito(sender, app_data, user_data):
    asiento = user_data[0]
    gestor_cine = user_data[1]
    tag_asiento = asiento.get_tag()

    tema_disponible, tema_seleccionado, tema_ocupado = crear_temas()
    if asiento.presionado == False:
        # print(f"Asiento seleccionado: {asiento.tag}")
        dpg.bind_item_theme(sender, tema_seleccionado)
        asiento.presionado = True
        gestor_cine.lista_compra_asientos.append(tag_asiento)

        gestor_cine.cant_boletas += 1
        dpg.configure_item("compra_info", default_value=f"Precio: {gestor_cine.cant_boletas * gestor_cine.precio_boleta}, Boletas: {gestor_cine.cant_boletas}")

        #Desactivar mensaje de error en caso de estar activo
        dpg.configure_item("Resultado_de_compra", show = False)
    else:
        # print(f"Asiento Des-seleccionado: {asiento.tag}")
        dpg.bind_item_theme(sender, tema_disponible)
        asiento.presionado = False
        gestor_cine.lista_compra_asientos.remove(tag_asiento)

        gestor_cine.cant_boletas -= 1
        dpg.configure_item("compra_info", default_value=f"Precio: {gestor_cine.cant_boletas * gestor_cine.precio_boleta}, Boletas: {gestor_cine.cant_boletas}")


class Asiento:
    def __init__(self, tag):
        self.__tag = tag
        self.presionado = False

    def get_tag(self):
        return self.__tag
