import dearpygui.dearpygui as dpg
from .clase_usuario import User
from Fachada.clase_fachade import Sistema_Cine
from Administrador.Interfaz_Administrador import open_popup_cartelera
from Funciones.funciones_generales_ventanas import close_popup_in_x_seconds

def hide_item(item):
    dpg.hide_item(item)

# Define la funcion para abrir la ventana emergente
def open_popup_sign_in(gestor_cine: Sistema_Cine):

    if gestor_cine.usuario_en_sesion:
        # Si ya esta autenticado, mostrar solo el boton de cerrar sesion
        dpg.configure_item("username", show=False)
        dpg.configure_item("password", show=False)
        dpg.configure_item("sign_in_button", show=False)
        dpg.configure_item("log_out_button", show=True)
        dpg.configure_item("create_account_direction", show=False)
        dpg.configure_item("message_text", default_value="Ya has iniciado sesion.")
        if gestor_cine.administrador_activo == True:
            text = f"Administrador: {gestor_cine.user.name}\nSaldo: {gestor_cine.user.saldo}"
        else:
            text = f"Usuario: {gestor_cine.user.name}\nSaldo: {gestor_cine.user.saldo}\n\nReservas:"

            # Si hay reservas, listarlas
            reservas = gestor_cine.user.reservations
            if reservas:
                for reserva in reservas:
                    text += f"\n- {reserva['hora_inicio']} - Asientos: {', '.join(reserva['lista_asientos'])}"
            else:
                text += "\nNo tienes reservas."

        dpg.configure_item("user_credentials", default_value=text, show=True)
    else:
        dpg.configure_item("mensaje_sesion_no_iniciada", show=False)
        # Mostrar los campos de entrada y boton de inicio de sesion
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

# Define la funcion de inicio de sesion
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
            dpg.configure_item("button_agregar_pelicula_admin", show=True)

            open_popup_cartelera(gestor_cine)

        else:
            gestor_cine.administrador_activo = False

        dpg.configure_item("iniciar_sesion_ventana_principal", label="Informacion Cuenta")
        dpg.configure_item("message_text", default_value="Inicio de sesion exitoso.")
        dpg.configure_item("create_account_direction", show=False)
        close_popup_in_x_seconds(2, "popup_window")  # Cerrar la ventana despues de 4 segundos
    else:
        dpg.configure_item("message_text", default_value="Credenciales incorrectas. Intente nuevamente.")
        dpg.configure_item("password", default_value="")

# Define la funcion de cerrar sesion
def log_out(sender, app_data, user_data):
    gestor_cine = user_data  # Obtener gestor_cine pasado como user_data
    gestor_cine.usuario_en_sesion = False
    gestor_cine.administrador_activo = False
    gestor_cine.user = None

    dpg.configure_item("message_text", default_value="Se ha cerrado la sesion.")
    dpg.configure_item("user_credentials", show=False, default_value="")
    dpg.configure_item("create_account_direction", show=True)
    dpg.configure_item("Info_admin_en_principal", show=False)
    dpg.configure_item("button_agregar_pelicula_admin", show=False)

    dpg.configure_item("iniciar_sesion_ventana_principal", label="Iniciar Sesion")

    dpg.show_item("create_account_direction") #Mostrar nuevamente el boton de crear cuenta
    close_popup_in_x_seconds(2, "popup_window")

# Crear la ventana emergente como una ventana modal oculta inicialmente
def setup_popup_signin_window(gestor_cine):
    from Objetos_Diseño.temas import crear_tema_global
    tema_blanco = crear_tema_global()

    with dpg.window(label="Inicio de Sesion", modal=True, show=False, tag="popup_window", width=600, height=150, pos=(400, 0)):
        dpg.bind_theme(tema_blanco)
        dpg.add_text("Ingrese sus credenciales", tag="message_text")  # Texto de mensaje
        dpg.add_text("", tag="user_credentials", show=False)
        dpg.add_input_text(tag="username", label="Correo")
        dpg.add_input_text(tag="password", label="Contraseña", password=True)

        # Boton para abrir la ventana de creacion de cuenta

        dpg.add_button(label="Iniciar sesion", tag="sign_in_button", callback=sign_in, user_data=gestor_cine)
        # Boton para cerrar sesion
        dpg.add_button(label="Cerrar sesion", tag="log_out_button", callback=log_out, show=False, user_data=gestor_cine)





