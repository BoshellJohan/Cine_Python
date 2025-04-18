import dearpygui.dearpygui as dpg
from Funciones.funciones_generales_ventanas import cerrar_ventana_reservas_in_x_segundos

def comprobar_compra(sender, app_data, user_data):
    gestor_cine = user_data[0]
    obj_sala = user_data[1]
    hora_inicio = user_data[2]
    ventana_tag = user_data[3]
    precio_a_pagar = gestor_cine.cant_boletas * gestor_cine.precio_boleta

    if len(gestor_cine.lista_compra_asientos) > 0 and gestor_cine.cant_boletas > 0:
        if gestor_cine.user.saldo > precio_a_pagar:
            #Guardar en el archivo la lista de asientos reservados
            obj_sala.agregar_asientos_ocupados(hora_inicio, gestor_cine.lista_compra_asientos)
            gestor_cine.guardar_salas_archivo()

            #Guardar en el archivo la informacion de la reserva del usuario y Actualizar saldo
            gestor_cine.user.agregar_reserva(hora_inicio, gestor_cine.lista_compra_asientos)
            gestor_cine.user.saldo -= precio_a_pagar
            gestor_cine.guardar_usuarios_archivo()

            dpg.configure_item("Resultado_de_compra", show = True, default_value="Compra realizada con exito.", color=(93, 162, 51, 255))
            
            cerrar_ventana_reservas_in_x_segundos(3, ventana_tag, obj_sala)
        else:
            dpg.configure_item("Resultado_de_compra", show = True, default_value="El saldo de la tarjeta no es suficiente para pagar las boletas.", color=(255,0,0, 255))

    else:
        dpg.configure_item("Resultado_de_compra", show = True, default_value="No se han seleccionado asientos para comprar.", color=(255,0,0, 255))


