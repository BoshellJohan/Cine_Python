import dearpygui.dearpygui as dpg
import threading
from .clase_usuario import User
from Fachada.clase_fachade import Sistema_Cine



# Función de temporizador para cerrar la ventana después de 4 segundos
def close_popup_in_x_seconds(sec, window):
    threading.Timer(sec, lambda: dpg.hide_item(window)).start()

def hide_item(item):
    dpg.hide_item(item)

# Define la función para abrir la ventana emergente
def open_popup_sign_in(gestor_cine: Sistema_Cine):
    if gestor_cine.usuario_en_sesion:
        # Si ya está autenticado, mostrar solo el botón de cerrar sesión
        dpg.configure_item("username", show=False)
        dpg.configure_item("password", show=False)
        dpg.configure_item("sign_in_button", show=False)
        dpg.configure_item("log_out_button", show=True)
        dpg.configure_item("create_account_direction", show=False)
        dpg.configure_item("message_text", default_value="Ya has iniciado sesión.")
        if gestor_cine.administrador_activo == True:
            text = f"Administrador: {gestor_cine.user.name}\nSaldo: {gestor_cine.user.saldo}"
        else:
            text = f"Usuario: {gestor_cine.user.name}\nSaldo: {gestor_cine.user.saldo}"
        dpg.configure_item("user_credentials", default_value=text, show=True)
    else:
        # Mostrar los campos de entrada y botón de inicio de sesión
        dpg.configure_item("username", show=True)
        dpg.set_value("username", "")
        dpg.configure_item("password", show=True)
        dpg.set_value("password", "")
        dpg.configure_item("sign_in_button", show=True)
        dpg.configure_item("log_out_button", show=False)
        dpg.configure_item("create_account_direction", show=True)
        dpg.configure_item("message_text", default_value="Ingrese sus credenciales.")
        dpg.configure_item("user_credentials", default_value="", show=False)

    dpg.show_item("popup_window")

# Define la función de inicio de sesión
def sign_in(sender, app_data, user_data):
    gestor_cine = user_data  # Obtener gestor_cine pasado como user_data
    username = dpg.get_value("username")
    password = dpg.get_value("password")

    user = gestor_cine.is_user_in_DB(username, password)

    if user != False:
        gestor_cine.usuario_en_sesion = True
        gestor_cine.user = user

        if user.esAdministrador: #Es administrador?
            gestor_cine.administrador_activo = True
            dpg.configure_item("Info_admin_en_principal", show=True)
            gestor_cine.ver_info_admins()
        else:
            gestor_cine.administrador_activo = False

        dpg.configure_item("message_text", default_value="Inicio de sesión exitoso.")
        dpg.configure_item("create_account_direction", show=False)
        close_popup_in_x_seconds(2, "popup_window")  # Cerrar la ventana después de 4 segundos
    else:
        dpg.configure_item("message_text", default_value="Credenciales incorrectas. Intente nuevamente.")
        dpg.configure_item("password", default_value="")

# Define la función de cerrar sesión
def log_out(sender, app_data, user_data):
    gestor_cine = user_data  # Obtener gestor_cine pasado como user_data
    gestor_cine.usuario_en_sesion = False
    gestor_cine.administrador_activo = False
    gestor_cine.user = None

    dpg.configure_item("message_text", default_value="Se ha cerrado la sesión.")
    dpg.configure_item("user_credentials", show=False, default_value="")
    dpg.configure_item("create_account_direction", show=True)
    dpg.configure_item("Info_admin_en_principal", show=False)

    dpg.show_item("create_account_direction") #Mostrar nuevamente el botón de crear cuenta
    close_popup_in_x_seconds(2, "popup_window")

# Crear la ventana emergente como una ventana modal oculta inicialmente
def setup_popup_signin_window(gestor_cine):
    with dpg.window(label="Inicio de Sesión", modal=True, show=False, tag="popup_window", width=500, height=200, pos=(800, 0)):
        dpg.add_text("Ingrese sus credenciales", tag="message_text")  # Texto de mensaje
        dpg.add_text("", tag="user_credentials", show=False)
        dpg.add_input_text(tag="username", label="Correo")
        dpg.add_input_text(tag="password", label="Contraseña", password=True)

        # Botón para abrir la ventana de creación de cuenta

        dpg.add_button(label="Iniciar sesión", tag="sign_in_button", callback=sign_in, user_data=gestor_cine)
        # Botón para cerrar sesión
        dpg.add_button(label="Cerrar sesión", tag="log_out_button", callback=log_out, show=False, user_data=gestor_cine)

