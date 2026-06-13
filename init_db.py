import sqlite3
DB_NAME = "certificados.db"

def  crear_base_de_datos():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumnos (
            dni TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            carrera TEXT NOT NULL,
            estado TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solicitudes (
            id_solicitud INTEGER PRIMARY KEY AUTOINCREMENT,
            dni TEXT NOT NULL,
            carrera TEXT NOT NULL,
            fecha_solicitud TEXT NOT NULL,
            estado_solicitud TEXT NOT NULL,
            FOREIGN KEY (dni) REFERENCES alumnos(dni)
        )
    """)

    alumnos = [
        ("40111222", "Juan", "Perez", "Tecnicatura Universitaria en Programacion", "Activo", "juan.perez@email.com"),
        ("39222333", "Ana", "Gomez", "Tecnicatura Universitaria en Programacion", "Inactivo", "ana.gomez@email.com"),
        ("42123456", "Lucia", "Fernandez", "Tecnicatura Universitaria en Programacion", "Activo", "lucia.fernandez@email.com"),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO alumnos (dni, nombre, apellido, carrera, estado, email)
        VALUES (?, ?, ?, ?, ?, ?)
    """, alumnos)

    conexion.commit()
    conexion.close()

    print("Base de datos creada correctamente.")


if __name__ == "__main__":
    crear_base_de_datos()