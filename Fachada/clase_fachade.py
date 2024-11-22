import json
from Interfaz_Usuario.clase_usuario import User
from Reservas_Salas.clases_reservas import Gestor_Archivo_Salas
from Peliculas.clases_pelicula import Gestor_Archivo_Peliculas, Pelicula

class Sistema_Cine:
    def __init__(self, filepath_users, filepath_salas, filepath_peliculas):
        #Atributos referentes a Usuarios
        self.lista_usuarios = []
        self.usuario_en_sesion = False
        self.user = None
        self.archivo_usuarios = Gestor_Archivo_Usuarios(filepath_users)  # Cargar desde el archivo
        self.administrador_activo = None

        #Atributos referentes a Salas y Reservas
        self.archivo_salas = Gestor_Archivo_Salas(filepath_salas)
        self.lista_salas = []
        self.lista_compra_asientos = []
        self.cant_boletas = 0
        self.precio_boleta = 45

        #Atributos referentes a Peliculas
        self.archivo_peliculas = Gestor_Archivo_Peliculas(filepath_peliculas)
        self.lista_peliculas = []


    def existencia_usuario(self, nuevo_usuario):
        for usuario in self.lista_usuarios:
            email_user = usuario.get_email()
            email_new_user = nuevo_usuario.get_email()

            if email_new_user.lower() == email_user.lower():
                return True
        return False

    def is_user_in_DB(self, email_client, password_client):
        for usuario in self.lista_usuarios:
            email_user = usuario.get_email()
            password_user = usuario.get_password()
            if email_user.lower() == email_client.lower() and password_user == password_client:
                return usuario
        return False

    def agregar_nuevo_usuario(self, usuario):
        if not self.existencia_usuario(usuario):
            self.lista_usuarios.append(usuario)
            self.guardar_usuarios_archivo()
            return True
        return False

    def guardar_usuarios_archivo(self):
        # Guardar usuarios en el archivo
        self.archivo_usuarios.guardar_usuarios(self.lista_usuarios)

    def cargar_usuarios_archivo(self):
        # Cargar usuarios desde el archivo
        self.lista_usuarios = self.archivo_usuarios.cargar_usuarios()

    #Metodos referentes a las salas
    def cargar_salas_archivo(self):
        self.lista_salas = self.archivo_salas.cargar_salas()

    def guardar_salas_archivo(self):
        self.archivo_salas.guardar_salas(self.lista_salas)

    #Metodos referentes a las peliculas
    def cargar_peliculas_archivo(self):
        self.lista_peliculas = self.archivo_peliculas.cargar_peliculas()

    def guardar_peliculas_archivo(self):
        self.archivo_peliculas.guardar_peliculas(self.lista_peliculas)

    def agregar_pelicula_lista(self, nombre, descripcion, duracion):
        self.lista_peliculas.append(Pelicula(nombre, descripcion, duracion, []))
        self.guardar_peliculas_archivo()



class Gestor_Archivo_Usuarios:
    def __init__(self, filepath):
        self.filepath = filepath

    def guardar_usuarios(self, lista_usuarios):
        # Convertir cada objeto `User` a diccionario para almacenar en JSON
        usuarios_data = [self._usuario_a_diccionario(usuario) for usuario in lista_usuarios]

        # Escribir datos de usuarios en el archivo JSON
        with open(self.filepath, 'w') as file:
            json.dump(usuarios_data, file, indent=4)
        print("Usuarios guardados exitosamente.")

    def cargar_usuarios(self):
        # Leer datos de usuarios desde el archivo JSON y reconstruir objetos `User`
        try:
            with open(self.filepath, 'r') as file:
                usuarios_data = json.load(file)
                return [self._diccionario_a_usuario(data) for data in usuarios_data]
        except FileNotFoundError:
            print("Archivo no encontrado. Se cargara una lista vacia.")
            return []

    def _usuario_a_diccionario(self, usuario):
        # Convertir un objeto `User` en un diccionario
        return {
            "name": usuario.name,
            "email": usuario.get_email(),
            "password": usuario.get_password(),
            "num_Card": usuario.tarjeta.numero,
            "saldo": usuario.saldo,
            "esAdministrador": usuario.esAdministrador,
            "reservations": usuario.reservations
        }

    def _diccionario_a_usuario(self, data):
        # Convertir un diccionario a un objeto `User`
        return User(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            num_Card=data["num_Card"],
            saldo=data["saldo"],
            esAdministrador=data["esAdministrador"],
            reservations=data["reservations"]
        )
















