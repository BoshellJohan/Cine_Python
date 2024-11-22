import dearpygui.dearpygui as dpg

class Tarjeta:
    def __init__(self, numero):
        self.numero = numero
        self.saldo = 1000


class User:
    def __init__(self, name, email, password, num_Card, saldo, esAdministrador, reservations):
        self.name = name
        self.__email = email
        self.__password = password
        self.tarjeta = Tarjeta(num_Card)
        self.reservations = reservations
        self.esAdministrador = esAdministrador
        self.saldo = saldo

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email

    def agregar_reserva(self, hora_inicio, lista_asientos):
        self.reservations.append({"hora_inicio": hora_inicio, "lista_asientos": lista_asientos})


class Administrador(User):
    def __init__(self, name, email, password, num_Card, reservations, esAdministrador):
        super().__init__(name, email, password, num_Card, reservations)
        self.esAdministrador = True

