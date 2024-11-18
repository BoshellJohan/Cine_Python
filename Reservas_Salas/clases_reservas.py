import json
import math


class Sala:
    def __init__(self, numero_sala: int, capacidad_max: int, letra_max: chr, numeracion_maxima: int, horarios: dict):
        self.numero_sala = numero_sala
        self.capacidad_max = capacidad_max
        self.letra_max = letra_max
        self.numeracion_maxima = numeracion_maxima
        self.horarios = horarios

    def ordenar_horarios_sala(self):
        # Ordenar las claves (horas) del diccionario en formato de hora
        horarios_ordenados = dict(sorted(self.horarios.items(), key=lambda x: x[0]))
        self.horarios = horarios_ordenados
        print("Horarios de la sala ordenados por hora de inicio.")


    def agregar_horario_funcion(self, hora_inicio):
        if hora_inicio in self.horarios:
            print(f"El horario {hora_inicio} ya existe para esta sala.")
        else:
            self.horarios[hora_inicio] = {"asientos_ocupados": []}
            self.ordenar_horarios_sala()
            print(f"Horario {hora_inicio} agregado exitosamente para la sala.")


    def agregar_asientos_ocupados(self, hora_de_inicio, asientos):
        if hora_de_inicio in self.horarios:
            self.horarios[hora_de_inicio]["asientos_ocupados"].extend(asientos)
        else:
            print("Horario no encontrado.")

    def verificar_disponibilidad_horarios(self, hora_inicio, duracion):
        """
        Verifica si un nuevo horario puede agregarse sin superponer con los existentes.
        :param hora_inicio: Hora de inicio de la nueva función en formato "HH:MM".
        :param duracion: Duración de la nueva función en minutos.
        :return: True si el horario está disponible, False en caso contrario.
        """
        # Convertir la hora de inicio a minutos
        hora_inicio_minutos = int(hora_inicio[:2]) * 60 + int(hora_inicio[3:])
        hora_fin_minutos = hora_inicio_minutos + int(duracion)

        # Iterar sobre los horarios existentes
        for horario_existente in self.horarios.keys():
            # Convertir la hora existente a minutos
            hora_existente_minutos = int(horario_existente[:2]) * 60 + int(horario_existente[3:])
            hora_existente_fin = hora_existente_minutos + 180  # Supone duración estándar de 2 horas

            # Verificar superposición
            if not (hora_fin_minutos <= hora_existente_minutos or hora_inicio_minutos >= hora_existente_fin):
                print(f"Conflicto con el horario existente: {horario_existente}")
                return False

        # Si no hay conflictos, el horario está disponible
        print(f"El horario solicitado está disponible en la sala {self.numero_sala}.")
        return True


    def verificar_disponibilidad_asientos(self, hora, asiento):
        if hora in self.horarios:
            return asiento not in self.horarios[hora]["asientos_ocupados"]
        return False


class Gestor_Archivo_Salas:
    def __init__(self, filepath):
        self.filepath = filepath

    def guardar_salas(self, lista_salas):
        salas_data = [self._sala_a_diccionario(sala) for sala in lista_salas]
        with open(self.filepath, 'w') as file:
            json.dump(salas_data, file, indent=4)
        print("Salas guardadas exitosamente.")

    def cargar_salas(self):
        try:
            with open(self.filepath, 'r') as file:
                salas_data = json.load(file)
                return [self._diccionario_a_sala(data) for data in salas_data]
        except FileNotFoundError:
            print("Archivo no encontrado. Se cargará una lista vacía.")
            return []

    def _sala_a_diccionario(self, sala: Sala):
        return {
            "numero_sala": sala.numero_sala,
            "capacidad_max": sala.capacidad_max,
            "letra_max": sala.letra_max,
            "numeracion_maxima": sala.numeracion_maxima,
            "horarios": sala.horarios  # No es necesario procesar más allá
        }

    def _diccionario_a_sala(self, data):
        return Sala(
            numero_sala=data["numero_sala"],
            capacidad_max=data["capacidad_max"],
            letra_max=data["letra_max"],
            numeracion_maxima=data["numeracion_maxima"],
            horarios=data["horarios"]
        )



