import dearpygui.dearpygui as dpg

class Tarjeta:
    def __init__(self, numero):
        self.numero = numero
        self.saldo = 1000


class User:
    def __init__(self, name, email, password, num_Card, saldo, esAdministrador, reservations):
        self.name = name
        self.email = email
        self.password = password
        self.tarjeta = Tarjeta(num_Card)
        self.reservations = reservations
        self.esAdministrador = esAdministrador
        self.saldo = self.tarjeta.saldo


    def consultar_saldo(self):
        return f"El saldo del usuario {self.name} es de ${self.tarjeta.saldo}.\n"

    def ver_reservas(self):
        ## Estructura de una reserva
        ## {sala: 4, horario: "13:00", asientos: [A1, A2, A3]}
        for clave, valor in self.reservations.items():
            if clave == "sala":
                print(f"Sala: {valor}, ", end="")
            elif clave == "horario":
                print(f"Hora de inicio: {valor}")
            else:
                print("Asientos: ", end="")
                for asiento in valor:
                    print(f"{asiento}\t", end=" ")

    def agregar_reserva(self, hora_inicio, lista_asientos):
        self.reservations.append({"hora_inicio": hora_inicio, "lista_asientos": lista_asientos})


class Administrador(User):
    def __init__(self, name, email, password, num_Card, reservations, esAdministrador):
        super().__init__(name, email, password, num_Card, reservations)
        self.esAdministrador = True

