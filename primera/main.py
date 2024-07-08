import sqlite3
import flet as ft

# Configuración de la base de datos SQLite
def setup_database():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    # Insertar usuarios de prueba
    cursor.execute("INSERT OR IGNORE INTO usuarios (username, password) VALUES ('danesalfari', 'danieles123')")
    cursor.execute("INSERT OR IGNORE INTO usuarios (username, password) VALUES ('danesari', '123456')")
    conn.commit()
    conn.close()

# Función para verificar credenciales
def verify_credentials(username, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Configuración de la aplicación Flet
def main(page: ft.Page):
    page.title = "Login"

    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True)
    message = ft.Text()

    def login(e):
        user = username.value
        pwd = password.value
        if verify_credentials(user, pwd):
            message.value = f"Welcome, {user}!"
            message.color = ft.colors.GREEN
        else:
            message.value = "Error: Invalid credentials."
            message.color = ft.colors.RED
        page.update()

    login_button = ft.ElevatedButton(text="Login", on_click=login)

    page.add(username, password, login_button, message)

# Crear y configurar la base de datos
setup_database()

# Iniciar la aplicación Flet
ft.app(target=main)