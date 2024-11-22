import dearpygui.dearpygui as dpg

def crear_temas():
    # Tema para los botones disponibles (color por defecto)
    with dpg.theme() as tema_disponible:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (66, 150, 250, 255))  # Azul predeterminado
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (40, 176, 227, 255))  # Color al pasar el mouse
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (40, 176, 227, 255))  # Color al hacer clic

    # Tema para los botones seleccionados (color verde)
    with dpg.theme() as tema_seleccionado:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (93, 162, 51, 255))  # Verde
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (107, 181, 62, 255))  # Color al pasar el mouse

    # Tema para los botones ocupados (color gris) y deshabilitados
    with dpg.theme() as tema_ocupado:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (128, 128, 128, 255))  # Gris
            dpg.add_theme_color(dpg.mvThemeCol_Text, (200, 200, 200, 255))  # Texto negro
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)  # Bordes redondeados
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (128, 128, 128, 255))  # Color al pasar el mouse

    return tema_disponible, tema_seleccionado, tema_ocupado



def crear_tema_global():
    with dpg.theme() as tema_global:
        # Fondo de la ventana principal (color blanco)
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 251, 254, 255))  # Fondo blanco
            dpg.add_theme_color(dpg.mvThemeCol_Text, (200, 200, 200, 255))  # Texto negro

        # Ajustar propiedades de botones o componentes adicionales si es necesario
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (147, 22, 33, 255))  # Color del boton
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (187, 42, 54, 255))  # Color al pasar el mouse
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (152, 33, 43, 255))  # Color al hacer clic
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)  # Bordes redondeados
            dpg.add_theme_color(dpg.mvThemeCol_Text, (200, 200, 200, 255))  # Texto negro

         # Otros estilos globales (sin tamaño de texto)
        with dpg.theme_component(dpg.mvWindowAppItem):
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 20)  # Padding

    return tema_global



def tema_input_claro():
    # Crear un tema personalizado para el input_text
    with dpg.theme() as tema_input_claro:
        with dpg.theme_component(dpg.mvInputText):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255, 255))  # Fondo blanco
            dpg.add_theme_color(dpg.mvThemeCol_Border, (96, 99, 94, 255))     # Borde naranja
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1.0)           # Grosor del borde
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3.0)             # Bordes redondeados
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255))  # Texto negro
    return tema_input_claro
