from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

alumnos = {
    "40111222": {
        "nombre": "Juan",
        "apellido": "Perez",
        "carrera": "Tecnicatura Universitaria en Programacion",
        "estado": "Activo"
    },
    "39222333": {
        "nombre": "Ana",
        "apellido": "Gomez",
        "carrera": "Tecnicatura Universitaria en Programacion",
        "estado": "Inactivo"
    }
}


def validar_dni(dni):
    if len(dni) != 8:
        return False
    if not dni.isdigit():
        return False
    return True


def dni_en_bd(dni):
    if dni in alumnos:
        return True
    return False


def validar_activo(dni):
    if alumnos[dni]["estado"] == "Activo":
        return True
    return False


def obtener_datos_alumno(dni):
    nombre = "Nombre"
    apellido = "Apellido"
    carrera = "carrera"
    return nombre, apellido, carrera


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
            return jsonify({
                "respuesta": "Certificado de alumno regular solicitado con éxito. En breve recibirá un correo con el certificado adjunto. Gracias por utilizar el sistema.",
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