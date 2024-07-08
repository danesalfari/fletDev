import mysql.connector
import flet as ft

# Configuración de la conexión a la base de datos MySQL
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        database='segunda'
    )

# Función para obtener productos de la base de datos
def fetch_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tienda")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Configuración de la aplicación Flet
def main(page: ft.Page):
    page.title = "tienda"

    # Tabla para mostrar los productos
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Precio Unitario")),
        ],
        rows=[]
    )

    # Función para cargar productos y actualizar la tabla
    def load_products(e):
        products = fetch_products()
        data_table.rows.clear()
        for product in products:
            data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(product[0]))),
                        ft.DataCell(ft.Text(product[1])),
                        ft.DataCell(ft.Text(str(product[2]))),
                        ft.DataCell(ft.Text(f"${product[3]:.2f}")),
                    ]
                )
            )
        page.update()

    load_button = ft.ElevatedButton(text="Cargar Productos", on_click=load_products)

    page.add(load_button, data_table)

# Iniciar la aplicación Flet
ft.app(target=main)