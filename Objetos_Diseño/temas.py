import dearpygui.dearpygui as dpg

def crear_temas():
    # Tema para los botones disponibles (color por defecto)
    with dpg.theme() as tema_disponible:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (66, 150, 250, 255))  # Azul predeterminado

    # Tema para los botones seleccionados (color verde)
    with dpg.theme() as tema_seleccionado:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 255, 0, 255))  # Verde

    # Tema para los botones ocupados (color gris)
    with dpg.theme() as tema_ocupado:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (128, 128, 128, 255))  # Gris

    return tema_disponible, tema_seleccionado, tema_ocupado