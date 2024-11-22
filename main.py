import dearpygui.dearpygui as dpg
from Interfaz_Usuario.inicio_sesion import open_popup_sign_in, setup_popup_signin_window
from Interfaz_Usuario.creacion_cuenta import setup_popup_create_account_window, open_popup_create_account
from Fachada.clase_fachade import Sistema_Cine
from Peliculas.Interfaz_Cartelera import mostrar_cartelera
from Administrador.Interfaz_Administrador import open_popup_cartelera
from Objetos_Diseño.temas import crear_tema_global



def main():

    # Inicializar DearPyGui
    dpg.create_context()
    dpg.create_viewport(title="Aplicacion de Inicio de Sesion", width=800, height=600)

    # Crear el tema global
    tema_blanco = crear_tema_global()

    # Aplicar el tema global a todo el programa
    dpg.bind_theme(tema_blanco)

    # Cargar la imagen y obtener sus detalles
    width, height, channels, data = dpg.load_image("./Img/images.jpg")

    # Crear la textura a partir de la imagen cargada
    with dpg.texture_registry(show=True):
        dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")


    filepath_salas = "./Reservas_Salas/salas.dat"
    filepath_users = "./Fachada/usuarios.dat"
    filepath_peliculas = "./Peliculas/peliculas.dat"

    # Crear una instancia de Sistema_Cine
    gestor_cine = Sistema_Cine(filepath_users, filepath_salas, filepath_peliculas)
    gestor_cine.cargar_usuarios_archivo()
    gestor_cine.cargar_salas_archivo()
    gestor_cine.cargar_peliculas_archivo()


    with dpg.window(label="Ventana Principal", width=1600, height=800, no_title_bar=True, no_move=True):
        # Seccion superior: Botones de inicio y creacion de cuenta
        with dpg.group(horizontal=True):
            dpg.add_button(label="Iniciar sesion", tag="iniciar_sesion_ventana_principal",callback=lambda: open_popup_sign_in(gestor_cine))
            dpg.add_button(label="Crear una cuenta", tag="create_account_direction", callback=lambda: open_popup_create_account(gestor_cine))

            # Texto de informacion del administrador
            dpg.add_text("Administrador activo", show=False, tag="Info_admin_en_principal", color=(93, 162, 51, 255))




        # Espaciador para separar la cartelera
        dpg.add_spacer(height=30)

        # Seccion inferior: Cartelera de peliculas
        with dpg.group(horizontal=False):
            dpg.add_text("Cartelera de Peliculas", color=(0, 0, 0, 255), bullet=True)
            mostrar_cartelera(gestor_cine)
            open_popup_cartelera(gestor_cine)






    # Configurar la ventana emergente para el inicio de sesion y creacion de cuenta
    setup_popup_create_account_window(gestor_cine)
    setup_popup_signin_window(gestor_cine)


    # Mostrar y mantener la ventana abierta

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()

    # Limpiar el contexto al cerrar la aplicacion
    dpg.destroy_context()




if __name__ == "__main__":
    main()