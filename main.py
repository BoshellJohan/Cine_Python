import dearpygui.dearpygui as dpg
from Interfaz_Usuario.inicio_sesion import open_popup_sign_in, setup_popup_signin_window
from Interfaz_Usuario.creacion_cuenta import setup_popup_create_account_window, open_popup_create_account
from Fachada.clase_fachade import Sistema_Cine
from Peliculas.Interfaz_Cartelera import open_popup_cartelera, mostrar_cartelera

# Inicializar DearPyGui
dpg.create_context()
dpg.create_viewport(title="Aplicación de Inicio de Sesión", width=800, height=600)

filepath_salas = "./Reservas_Salas/salas.dat"
filepath_users = "./Fachada/usuarios.dat"
filepath_peliculas = "./Peliculas/peliculas.dat"

# Crear una instancia de Sistema_Cine
gestor_cine = Sistema_Cine(filepath_users, filepath_salas, filepath_peliculas)
gestor_cine.cargar_usuarios_archivo()
gestor_cine.cargar_salas_archivo()
gestor_cine.cargar_peliculas_archivo()


with dpg.window(label="Ventana Principal", width=1600, height=800):
    # Sección superior: Botones de inicio y creación de cuenta
    with dpg.group(horizontal=False):
        dpg.add_button(label="Iniciar sesión", callback=lambda: open_popup_sign_in(gestor_cine))
        dpg.add_button(label="Crear una cuenta", tag="create_account_direction", callback=lambda: open_popup_create_account(gestor_cine))

    # Espaciador para separar visualmente
    dpg.add_spacer(height=20)

    # Texto de información del administrador
    dpg.add_text("Administrador activo", show=False, tag="Info_admin_en_principal", color=(0, 255, 0, 255))

    # Espaciador para separar la cartelera
    dpg.add_spacer(height=30)

    # Sección inferior: Cartelera de películas
    with dpg.group(horizontal=False):
        dpg.add_text("Cartelera de Películas", color=(255, 255, 255, 255), bullet=True)
        mostrar_cartelera(gestor_cine)
        open_popup_cartelera(gestor_cine)







# Configurar la ventana emergente para el inicio de sesión y creación de cuenta
setup_popup_create_account_window(gestor_cine)
setup_popup_signin_window(gestor_cine)



# Mostrar y mantener la ventana abierta

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

# Limpiar el contexto al cerrar la aplicación
dpg.destroy_context()
