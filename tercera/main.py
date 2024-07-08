from pymongo import MongoClient
import flet as ft

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["basededatos"]
collection = db["sensor"]

# Verificar e insertar datos del sensor si no están presentes
sensor = collection.find_one({"ID": "s1"})
if sensor is None:
    sensor_data = {
        "ID": "s1",
        "nombre": "sensor1",
        "minimo": 25,
        "maximo": 45,
        "Valores": [28, 29, 30, 31,]
    }
    collection.insert_one(sensor_data)
    sensor = sensor_data

# Extraer datos del sensor
sensor_id = sensor["ID"]
sensor_name = sensor["nombre"]
min_value = sensor["minimo"]
max_value = sensor["maximo"]
sensor_values = sensor["Valores"]

def highlight_value(value):
    if value < min_value or value > max_value:
        return ft.Text(str(value), color=ft.colors.RED)
    else:
        return ft.Text(str(value), color=ft.colors.GREEN)

def add_value(e):
    new_value = int(value_input.value)
    collection.update_one({"ID": "s1"}, {"$push": {"Valores": new_value}})
    sensor_values.append(new_value)
    value_input.value = ""
    value_input.update()
    values_list.controls.append(highlight_value(new_value))
    values_list.update()

def delete_value(e):
    try:
        value_to_delete = int(delete_input.value)
        if value_to_delete in sensor_values:
            collection.update_one({"ID": "s1"}, {"$pull": {"Valores": value_to_delete}})
            sensor_values.remove(value_to_delete)
            update_values_list()
        delete_input.value = ""
        delete_input.update()
    except ValueError:
        delete_input.value = "Invalid number"
        delete_input.update()

def update_values_list():
    values_list.controls.clear()
    for value in sensor_values:
        values_list.controls.append(highlight_value(value))
    values_list.update()

def main(page: ft.Page):
    global value_input, values_list, delete_input
    
    page.title = "Sensor Data"
    
    values_list = ft.Column([highlight_value(v) for v in sensor_values])
    
    value_input = ft.TextField(label="New Value", keyboard_type=ft.KeyboardType.NUMBER)
    submit_button = ft.ElevatedButton("Submit", on_click=add_value)

    delete_input = ft.TextField(label="Value to Delete", keyboard_type=ft.KeyboardType.NUMBER)
    delete_button = ft.ElevatedButton("Delete", on_click=delete_value)

    main_column = ft.Column(
        [
            ft.Text(f"ID: {sensor_id}"),
            ft.Text(f"Name: {sensor_name}"),
            ft.Text(f"Min Value: {min_value}"),
            ft.Text(f"Max Value: {max_value}"),
            values_list,
            value_input,
            submit_button,
            delete_input,
            delete_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    page.add(main_column)

ft.app(target=main)