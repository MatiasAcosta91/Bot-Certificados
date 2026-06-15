from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime


app = Flask(__name__)
DB_NAME = "certificados.db"


def validar_dni(dni):
    if len(dni) != 8:
        return False
    if not dni.isdigit():
        return False
    return True


def dni_en_bd(dni):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("SELECT dni FROM alumnos WHERE dni = ?", (dni,))
    alumno = cursor.fetchone()

    conexion.close()

    if alumno:
        return True
    return False


def validar_activo(dni):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("SELECT estado FROM alumnos WHERE dni = ?", (dni,))
    alumno = cursor.fetchone()

    conexion.close()

    if alumno and alumno[0] == "Activo":
        return True
    return False


def obtener_datos_alumno(dni):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT nombre, apellido, carrera FROM alumnos WHERE dni = ?",
        (dni,)
    )

    alumno = cursor.fetchone()
    conexion.close()

    nombre = alumno[0]
    apellido = alumno[1]
    carrera = alumno[2]

    return nombre, apellido, carrera


def registrar_solicitud(dni, carrera):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    fecha_actual = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    estado_solicitud = "Pendiente"

    cursor.execute("""
        INSERT INTO solicitudes (dni, carrera, fecha_solicitud, estado_solicitud)
        VALUES (?, ?, ?, ?)
    """, (dni, carrera, fecha_actual, estado_solicitud))

    numero_tramite = cursor.lastrowid

    conexion.commit()
    conexion.close()

    return numero_tramite

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    mensaje = data.get("mensaje", "").strip()
    estado = data.get("estado", "SOLICITAR_DNI")
    alumno_actual = data.get("alumno", None)

    if estado == "SOLICITAR_DNI":
        if mensaje == "0":
            return jsonify({
                "respuesta": "Gracias por utilizar el sistema. Hasta luego.",
                "estado": "FIN",
                "alumno": None
            })

        elif not validar_dni(mensaje):
            return jsonify({
                "respuesta": "DNI ingresado inválido.",
                "estado": "SOLICITAR_DNI",
                "alumno": None
            })

        elif not dni_en_bd(mensaje):
            return jsonify({
                "respuesta": "El DNI no se encuentra en la base de datos.",
                "estado": "SOLICITAR_DNI",
                "alumno": None
            })

        elif not validar_activo(mensaje):
            return jsonify({
                "respuesta": "El DNI ingresado no corresponde a un estudiante activo.",
                "estado": "FIN",
                "alumno": None
            })

        else:
            nombre, apellido, carrera = obtener_datos_alumno(mensaje)

            alumno_data = {
                "dni": mensaje,
                "nombre": nombre,
                "apellido": apellido,
                "carrera": carrera
            }

            return jsonify({
                "respuesta": f"DNI: {mensaje}<br>Nombre: {nombre}<br>Apellido: {apellido}<br>Carrera: {carrera}<br>¿Confirma solicitud? Responda SI o NO.",
                "estado": "CONFIRMAR_SOLICITUD",
                "alumno": alumno_data
            })

    if estado == "CONFIRMAR_SOLICITUD":
        if mensaje.lower() in ["si", "sí", "s"]:
            numero_tramite = registrar_solicitud(alumno_actual["dni"], alumno_actual["carrera"])
            return jsonify({
                "respuesta": f"Solicitud Generada, su numero de tramite es {numero_tramite}. En breve recibirá respuesta por email.",
                "estado": "FIN",
                "alumno": None
            })

        elif mensaje.lower() in ["no", "n"]:
            return jsonify({
                "respuesta": "Solicitud de certificado cancelada.",
                "estado": "FIN",
                "alumno": None
            })

        else:
            return jsonify({
                "respuesta": "Respuesta inválida. Por favor responda SI o NO.",
                "estado": "CONFIRMAR_SOLICITUD",
                "alumno": alumno_actual
            })

    return jsonify({
        "respuesta": "La conversación ya finalizó. Recargue la página para iniciar una nueva solicitud.",
        "estado": "FIN",
        "alumno": None
    })


if __name__ == "__main__":
    app.run(debug=True)