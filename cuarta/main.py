import mysql.connector
import flet as ft

# Configuración de la conexión a la base de datos MySQL
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        database='cuarta'
    )

# Función para obtener productos de la base de datos
def fetch_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Función para insertar un nuevo producto en la base de datos
def insert_product(codigo, nombre, cantidad, precio_unitario):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (codigo, nombre, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)", (codigo, nombre, cantidad, precio_unitario))
    conn.commit()
    conn.close()

# Configuración de la aplicación Flet
def main(page: ft.Page):
    page.title = "productos"

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

    # Formulario para ingresar los datos del producto
    product_form = ft.Column(
    controls=[
        ft.TextField(label="Código", width=100),
        ft.TextField(label="Nombre", width=200),
        ft.TextField(label="Cantidad", width=100),
        ft.TextField(label="Precio Unitario", width=100)
    ]
)

    # Botón para agregar el producto
    add_button = ft.ElevatedButton(text="Agregar Producto")

    def add_product(e):
        codigo = product_form.controls[0].value
        nombre = product_form.controls[1].value
        cantidad = int(product_form.controls[2].value)
        precio_unitario = float(product_form.controls[3].value)
        insert_product(codigo, nombre, cantidad, precio_unitario)
        load_products(None)  # Actualizar la tabla de productos

    add_button.on_click = add_product

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



    page.add(load_button, data_table, product_form, add_button)

# Iniciar la aplicación Flet
ft.app(target=main)