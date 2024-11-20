import dearpygui.dearpygui as dpg
import json

# Clase Pelicula
class Pelicula:
    def __init__(self, nombre, descripcion, duracion, horarios):
        self.nombre = nombre
        self.descripcion = descripcion
        self.duracion = duracion
        self.horarios = horarios


    def agregar_horario(self, hora_inicio, lista_salas):
        operacion = False
        for sala in lista_salas:
            if sala.verificar_disponibilidad_horarios(hora_inicio, self.duracion):
                sala.agregar_horario_funcion(hora_inicio)
                self.horarios.append({"sala": sala.numero_sala, "hora_inicio": hora_inicio})
                self.horarios = sorted(self.horarios, key=lambda x: x["hora_inicio"])
                operacion = True
                print("Se ha añadido el horario para la pelicula correctamente")
                break
        if not operacion:
            print(f"Ninguna sala esta disponible en ese horario para la pelicula {self.nombre}")





class Cartelera:
    def __init__(self, filepath):
        self.filepath = filepath


    def guardar_peliculas(self, lista_peliculas):
        try:
            # Convertir cada objeto `Pelicula` a diccionario para almacenar en JSON
            peliculas_data = [self._pelicula_a_diccionario(pelicula) for pelicula in lista_peliculas]

            # Escribir datos de películas en el archivo JSON
            with open(self.filepath, 'w') as file:
                json.dump(peliculas_data, file, indent=4)
            print("Películas guardadas exitosamente.")
        except Exception as e:
            print(f"Error al guardar las películas: {e}")



    def cargar_peliculas(self):
        try:
            # Leer datos de películas desde el archivo JSON
            with open(self.filepath, 'r') as file:
                peliculas_data = json.load(file)
                return [self._diccionario_a_pelicula(data) for data in peliculas_data]
        except FileNotFoundError:
            print("Archivo no encontrado. Se cargará una lista vacía.")
            return []
        except json.JSONDecodeError:
            print("Error: el archivo no tiene un formato JSON válido.")
            return []



    def _pelicula_a_diccionario(self, pelicula: Pelicula):
        # Convertir un objeto `User` en un diccionario
        return {
            "nombre": pelicula.nombre,
            "descripcion": pelicula.descripcion,
            "duracion": pelicula.duracion,
            "horarios": pelicula.horarios
        }

    def _diccionario_a_pelicula(self, data):
        # Convertir un diccionario a un objeto `User`
        return Pelicula(
            nombre=data["nombre"],
            descripcion=data["descripcion"],
            duracion=data["duracion"],
            horarios=data["horarios"]
        )

    #Eliminar al final
    def ver_peliculas(self, lista_peliculas):
        for pelicula in lista_peliculas:
            print(f"\nNombre: {pelicula.nombre}, Duracion: {pelicula.duracion}")
            for horario in pelicula.horarios:
                print(f"Horario {horario["hora_inicio"]} en la sala {horario["sala"]}")





