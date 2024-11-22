import threading
import dearpygui.dearpygui as dpg



# Funcion de temporizador para cerrar la ventana despues de 4 segundos
def close_popup_in_x_seconds(sec, window):
    threading.Timer(sec, lambda: dpg.hide_item(window)).start()

def cerrar_ventana_reservas_in_x_segundos(sec, ventana_tag, sala_funcion):
    threading.Timer(sec, lambda: eliminar_ventana_y_asientos(ventana_tag, sala_funcion)).start()


def eliminar_ventana_y_asientos(ventana_tag, sala_funcion):
    # Se asegura de que la eliminacion se haga en el hilo principal
    # dpg.add_item_dirty(ventana_tag)  # Esto asegura que se ejecuta en el hilo principal.

    # Eliminar la ventana
    dpg.delete_item(ventana_tag)

    # Eliminar todos los botones de asientos creados para esta ventana
    for letra in range(ord('A'), ord(sala_funcion.letra_max) + 1):
        for numero in range(1, sala_funcion.numeracion_maxima + 1):
            asiento_tag = f"{chr(letra)}{numero}_{sala_funcion.numero_sala}"
            if dpg.does_item_exist(asiento_tag):
                dpg.delete_item(asiento_tag)

