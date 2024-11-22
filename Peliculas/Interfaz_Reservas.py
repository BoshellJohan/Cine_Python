import dearpygui.dearpygui as dpg
from Reservas_Salas.clases_reservas import Sala
from Objetos_Diseño.temas import crear_temas
from Peliculas.Analisis_compra import comprobar_compra
from Funciones.funciones_generales_ventanas import cerrar_ventana_reservas_in_x_segundos


def mostrar_interfaz_reserva_de_horario(sender, app_data, user_data):
    #Resetear la lista de asientos elegidos
    gestor_cine = user_data[0]
    gestor_cine.lista_compra_asientos = []

    horario = user_data[1]
    nombre_pelicula = user_data[2]

    num_sala_de_funcion = horario['sala']
    hora_de_funcion = horario['hora_inicio']
    gestor_cine.cant_boletas = 0


    # Cerrar ventana de detalles de película si está abierta
    ventana_info_tag = f"window_{nombre_pelicula}"
    if dpg.does_item_exist(ventana_info_tag):
        dpg.hide_item(ventana_info_tag)

    ventana_tag = f"window_{num_sala_de_funcion}_{hora_de_funcion}"
    if dpg.does_item_exist(ventana_tag):
        dpg.delete_item(ventana_tag)

    with dpg.window(label=f"Reserva Horario - Sala {num_sala_de_funcion}", tag=ventana_tag, width=400, height=300, modal=False, no_close=True, no_resize=True, no_move=True):
        dpg.add_text(f"Reservas para la función de las {hora_de_funcion} en la sala {num_sala_de_funcion}")
        # Agregar el resto del código para manejar horarios y asientos
        for sala in gestor_cine.lista_salas:
            if sala.numero_sala == num_sala_de_funcion:
                sala_funcion = sala
                break
        print(f"Sala del horario: {num_sala_de_funcion}, Sala lógica: {sala.numero_sala}")
        if isinstance(sala_funcion, Sala):
            # Verificar si el horario existe en la sala
            if hora_de_funcion in sala.horarios:
                asientos_ocupados = sala.horarios[hora_de_funcion]["asientos_ocupados"]
                interfaz_sillas(sala, asientos_ocupados, gestor_cine)
                dpg.add_text(f"Precio: {gestor_cine.cant_boletas * gestor_cine.precio_boleta}, Boletas: {gestor_cine.cant_boletas}", tag=f"compra_info")
                dpg.add_button(label="Comprar boletas", callback=comprobar_compra, user_data=[gestor_cine, sala_funcion, hora_de_funcion, ventana_tag])
                dpg.add_text("", tag="Resultado_de_compra", show=False)
                print(f"Asientos ocupados para la función de las {hora_de_funcion}: {asientos_ocupados}")
            else:
                print(f"No se encontró la hora de función '{hora_de_funcion}'.")
        else:
            print("Error encontrando la sala del horario.")
        dpg.add_button(label="Cerrar", callback=lambda: cerrar_ventana_reservas_in_x_segundos(0, ventana_tag, sala_funcion))





def agregar_asiento_carrito(sender, app_data, user_data):
    asiento = user_data[0]
    gestor_cine = user_data[1]

    tema_disponible, tema_seleccionado, tema_ocupado = crear_temas()
    if asiento.presionado == False:
        print(f"Asiento seleccionado: {asiento.tag}")
        dpg.bind_item_theme(sender, tema_seleccionado)
        asiento.presionado = True
        gestor_cine.lista_compra_asientos.append(asiento.tag)

        gestor_cine.cant_boletas += 1
        dpg.configure_item("compra_info", default_value=f"Precio: {gestor_cine.cant_boletas * gestor_cine.precio_boleta}, Boletas: {gestor_cine.cant_boletas}")

        #Desactivar mensaje de error en caso de estar activo
        dpg.configure_item("Resultado_de_compra", show = False)
    else:
        print(f"Asiento Des-seleccionado: {asiento.tag}")
        dpg.bind_item_theme(sender, tema_disponible)
        asiento.presionado = False
        gestor_cine.lista_compra_asientos.remove(asiento.tag)

        gestor_cine.cant_boletas -= 1
        dpg.configure_item("compra_info", default_value=f"Precio: {gestor_cine.cant_boletas * gestor_cine.precio_boleta}, Boletas: {gestor_cine.cant_boletas}")



def interfaz_sillas(sala, asientos_ocupados, gestor_cine):
    letra_max = sala.letra_max
    numeracion_maxima = sala.numeracion_maxima
    tema_disponible, tema_seleccionado, tema_ocupado = crear_temas()  # Crear lo

    with dpg.group(horizontal=False):
        for letra in range(ord('A'), ord(letra_max) + 1):
            for numero in range(1, numeracion_maxima + 1):
                asiento = f"{chr(letra)}{numero}"
                if asiento in asientos_ocupados:
                    dpg.add_button(label=asiento, tag=f"{asiento}_{sala.numero_sala}")
                    dpg.bind_item_theme(f"{asiento}_{sala.numero_sala}", tema_ocupado)
                else:
                    obj_asiento = Asiento(asiento)
                    asiento_tag = f"{asiento}_{sala.numero_sala}"
                    dpg.add_button(label=asiento, tag=asiento_tag, callback=agregar_asiento_carrito, user_data=[obj_asiento, gestor_cine])
                    dpg.bind_item_theme(f"{asiento}_{sala.numero_sala}", tema_disponible)


class Asiento:
    def __init__(self, tag):
        self.tag = tag
        self.presionado = False
