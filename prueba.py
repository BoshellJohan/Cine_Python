sala = {
    "horarios": {
        "13:00": {
            "asientos_ocupados": ["A1", "A2", "A3", "B2", "B5"]
        },
        "16:00": {
            "asientos_ocupados": ["B2", "B5"]
        }
    }
}

hora_de_funcion = "13:00"  # Cambia esto para probar diferentes horas

# Verificar si la hora existe y obtener los asientos ocupados
if hora_de_funcion in sala["horarios"]:
    asientos_ocupados = sala["horarios"][hora_de_funcion]["asientos_ocupados"]
    print(f"Asientos ocupados para la función de las {hora_de_funcion}: {asientos_ocupados}")
else:
    print(f"No se encontró la hora de función '{hora_de_funcion}'.")
