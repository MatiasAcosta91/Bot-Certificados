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
    #en esta funcion se obtienen los datos de la base de datos
    nombre = "Nombre"
    apellido = "Apellido"
    carrera = "carrera"
    return nombre,apellido,carrera;

saludo = print("Hola, bienvenido al sistema de solicitudes de certificados de alumno regular:")

repetir = True

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

while repetir:
    dni = input("Ingrese su número de DNI o 0 para finalizar: ")
    if dni != "0":
        if validar_dni(dni):
            if dni_en_bd(dni):
                if validar_activo(dni):
                    nombre_alumno, apellido_alumno, carrera = obtener_datos_alumno(dni);
                    print(f" DNI: {dni} Nombre: {nombre_alumno}, Apellido: {apellido_alumno}, Carrera: {carrera}")
                    print("ingrese 'SI' para solicitar o 'NO' para cancelar.  ")
                    respuesta = input()
                    if respuesta.lower() == "si":
                        print("Certificado de alumno regular solicitado con éxito. El mismo sera enviado a su email a la brevedad")
                    else:
                        print("Solicitud de certificado cancelada. ¡Gracias por utilizar el sistema!")
                else:
                    print("El dni ingresado no corresponde a un estudiante activo.")        
            else:
                print("El dni no se encuentra en la base de datos.")
        else:
            print("DNI ingresado invalido.")
    else:
        print("Gracias por utilizar el sistema de solicitudes de certificados de alumno regular. ¡Hasta luego!")
        repetir = False



    
