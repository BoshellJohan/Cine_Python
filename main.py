import dearpygui.dearpygui as dpg
from Interfaz_Usuario.inicio_sesion import open_popup_sign_in, setup_popup_signin_window
from Interfaz_Usuario.creacion_cuenta import setup_popup_create_account_window, open_popup_create_account
from Fachada.clase_fachade import Sistema_Cine
from Peliculas.Interfaz_Cartelera import mostrar_cartelera

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


# Configuración de la ventana principal y el popup de inicio de sesión
with dpg.window(label="Ventana Principal", width=1500, height=1000):
    dpg.add_button(label="Iniciar sesión", callback=lambda: open_popup_sign_in(gestor_cine))
    dpg.add_button(label="Crear una cuenta", tag="create_account_direction", callback=lambda: open_popup_create_account(gestor_cine))
    dpg.add_text("Administrador activo", show=False, tag="Info_admin_en_principal", color=(0, 255, 0, 255))
    mostrar_cartelera(gestor_cine.lista_peliculas)




# Configurar la ventana emergente para el inicio de sesión y creación de cuenta
setup_popup_create_account_window(gestor_cine)
setup_popup_signin_window(gestor_cine)



# Mostrar y mantener la ventana abierta
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

# Limpiar el contexto al cerrar la aplicación
dpg.destroy_context()


