import threading
import dearpygui.dearpygui as dpg

# Función de temporizador para cerrar la ventana después de 4 segundos
def close_popup_in_x_seconds(sec, window):
    threading.Timer(sec, lambda: dpg.hide_item(window)).start()