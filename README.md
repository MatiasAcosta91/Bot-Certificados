# Bot de Certificados de Alumno Regular

Este proyecto es una simulacion web de un chatbot para solicitar certificados de alumno regular. Fue realizado para el Trabajo Practico Integrador de Organizacion Empresarial.

La idea del sistema es que un alumno pueda ingresar su DNI, el bot valide si existe en la base de datos, verifique si esta activo y luego permita confirmar la solicitud del certificado.

## Proceso trabajado

El proceso elegido fue la **solicitud de certificado de alumno regular** dentro de una institucion educativa.

Antes de automatizarlo, el alumno debia comunicarse con Administracion para pedir el certificado, enviar sus datos y esperar que el personal revisara manualmente la solicitud, si la informacion aportada era correcta se emitia el certificado, en caso contrario debia contactarse la administracion nuevamente con el alumno para solicitarle los datos corerctos

Con el bot, la primera parte del proceso queda automatizada:

- El alumno inicia el chat.
- El bot solicita el DNI.
- El sistema valida el formato del DNI.
- El sistema consulta si el alumno existe en la base de datos.
- El sistema verifica si el alumno esta activo.
- El alumno confirma o cancela la solicitud.
- Si confirma, se registra el tramite.

## Diagramas BPMN

### Proceso AS-IS
Este diagrama representa el proceso actual/manual, antes de implementar el bot.

<img width="573" height="510" alt="image" src="https://github.com/user-attachments/assets/94d5884b-f0c6-410e-afc6-8fb72ee47f26" />


### Proceso TO-BE


Este diagrama representa el proceso propuesto con el chatbot.

<img width="731" height="501" alt="image" src="https://github.com/user-attachments/assets/2ad3f65e-a5fb-4406-a84e-47e11109ff11" />

## Tecnologias utilizadas

- Python
- Flask
- SQLite
- HTML
- CSS
- Git y GitHub

Se eligio Flask porque permite hacer una aplicacion web simple sin usar un framework complejo. SQLite se uso como base de datos porque permite trabajar con tablas reales sin instalar un servidor externo.

## Base de datos

La base de datos utilizada es `certificados.db`.

Tiene dos tablas principales:

### Tabla alumnos

Se usa para validar si el DNI ingresado corresponde a un alumno registrado y si el alumno esta activo.

Campos principales:

- dni
- nombre
- apellido
- carrera
- estado
- email

### Tabla solicitudes

Se usa para guardar las solicitudes de certificado realizadas por los alumnos.

Campos principales:

- id_solicitud
- dni
- carrera
- fecha_solicitud
- estado_solicitud

## Capturas del sistema

### Pantalla inicial del bot

<img width="460" height="237" alt="image" src="https://github.com/user-attachments/assets/834511f9-04cf-44ad-8a1f-d9e228e36e4c" />


### Validacion de DNI correcto

<img width="401" height="305" alt="image" src="https://github.com/user-attachments/assets/b1a079f0-8bc1-4d28-93e7-fae9b041312a" />

### Solicitud confirmada

<img width="717" height="385" alt="image" src="https://github.com/user-attachments/assets/ea717b74-69d0-4d79-975e-8209b8ce73f8" />


### Ejemplo de DNI invalido

<img width="420" height="267" alt="image" src="https://github.com/user-attachments/assets/febbf850-ce24-4883-85ff-83ed4cdffe13" />

### Ejemplo de alumno inactivo

<img width="489" height="327" alt="image" src="https://github.com/user-attachments/assets/549381e1-09fc-4e63-8549-a4f85bc83ecc" />

## Como ejecutar el proyecto

1. Clonar el repositorio:

  git clone https://github.com/USUARIO/Bot-Certificados.git


2. Entrar a la carpeta:

  cd Bot-Certificados


3. Instalar dependencias:

  pip install -r requirements.txt


4. Crear la base de datos:

  python init_db.py


5. Ejecutar la aplicacion:

  python app.py


6. Abrir en el navegador:

  http://127.0.0.1:5000


## Datos para probar
DNI--------Situacion   
40111222  Alumno activo   
39222333  Alumno inactivo   
99999999  DNI no registrado  
abc  DNI invalido   

## Relacion con el BPMN

Cada decision del diagrama TO-BE se representa en el codigo mediante validaciones:

validar_dni() representa la decision "DNI valido?"  
dni_en_bd() representa la decision "DNI en BD?"  
validar_activo() representa la decision "Estudiante activo?"  
La confirmacion SI/NO representa la decision "Alumno responde si/no"  

De esta forma, el codigo sigue la misma logica que el proceso modelado.

## Estado del proyecto

El proyecto funciona como una simulacion del proceso. No emite un certificado real, sino que registra la solicitud y permite demostrar como se automatizaria el tramite administrativo.

## Autores
Acosta Matias, Gustavo Parodi
