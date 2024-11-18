# creacioncuenta.py
import dearpygui.dearpygui as dpg
from .clase_usuario import User
from .inicio_sesion import close_popup_in_x_seconds, hide_item
from Fachada.clase_fachade import Sistema_Cine


def clear_input_text(name_input, show_input=False):
    dpg.configure_item(name_input, show=show_input)

def open_popup_create_account(gestor_cine: Sistema_Cine):
    print("Usuario en sesión:", gestor_cine.usuario_en_sesion)
    if not gestor_cine.usuario_en_sesion:
        dpg.configure_item("create_name", show=True)
        dpg.set_value("create_name", "")
        dpg.configure_item("create_email", show=True)
        dpg.set_value("create_email", "")
        dpg.configure_item("create_password", show=True)
        dpg.set_value("create_password", "")
        dpg.configure_item("create_account_button", show=True)
        dpg.configure_item("message_error_account", show=False)

    dpg.show_item("popup_window_create_account")  # Muestra la ventana emergente


def save_new_user_in_DB(gestor_cine: Sistema_Cine, user):
    gestor_cine.usuario_en_sesion = True
    gestor_cine.user = user
    gestor_cine.agregar_nuevo_usuario(user) #Agregar usuario a la lista
    gestor_cine.guardar_usuarios_archivo() #Actualizar archivo
    # gestor_cine.ver_usuarios()



def create_account(sender, app_data, user_data):
    gestor_cine = user_data
    clear_input_text("message_error_account")

    name = dpg.get_value("create_name").strip()
    email = dpg.get_value("create_email").strip()
    password = dpg.get_value("create_password")

    if name != ""  and email != "" and password != "": #Inputs vacíos
        nuevo_usuario = User(name, email, password, "22222222000", 1200, False,[])

        print(gestor_cine.existencia_usuario(nuevo_usuario))

        if not gestor_cine.existencia_usuario(nuevo_usuario):
            save_new_user_in_DB(gestor_cine, nuevo_usuario)

            dpg.configure_item("create_name", show=False)
            dpg.configure_item("create_email", show=False)
            dpg.configure_item("create_password", show=False)
            dpg.configure_item("message_text_account", default_value="Cuenta creada exitosamente")
            close_popup_in_x_seconds(2,"popup_window_create_account")
            hide_item("create_account_button")
            hide_item("create_account_direction")
        else:
            dpg.set_value("create_email", "")
            dpg.configure_item("message_error_account", default_value=f"El correo {email} ya se encuentra registrado.", show=True, color=(255, 0, 0, 255))
    else:
        dpg.configure_item("message_error_account", default_value=f"Los campos no se han rellenado correctamente.", show=True, color=(255, 0, 0, 255))

def setup_popup_create_account_window(gestor_cine: Sistema_Cine):
    with dpg.window(label="Creacion de Cuenta", modal=True, show=False, tag="popup_window_create_account", width=800, height=400, pos=(1000, 400)):
        dpg.add_text("Ingrese sus datos: ", tag="message_text_account")
        dpg.add_input_text(tag="create_name", label="Nombre")
        dpg.add_input_text(tag="create_email", label="Email")
        dpg.add_input_text(tag="create_password", label="Contraseña")
        dpg.add_text(tag="message_error_account", label="", show=False)

        dpg.add_button(label="Crear cuenta", tag="create_account_button", callback=create_account, user_data=gestor_cine)
