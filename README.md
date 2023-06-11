# DSGTestBot (APIREST Telegram Bot)

Este proyecto es una solución que combina un bot de Telegram(DSGTestBot) y APIREST para leer todos los mensajes recibidos por el bot y el envio  mensajes a los usuarios que hayan interactuado con el bot.


# Funcionalidades
- Permite recibir mensajes de usuarios atraves del bot llamado DSGTestBot y almacenarlos en una base de datos MongoDB.
- Proporciona endpoints en una aplicación Flask para obtener y enviar mensajes a través de la API.


# Requisitos
- Python 3.7 o superior
- MongoDB instalado y en ejecución en localhost:27017
- Paquetes requeridos: telegram, pymongo, flask, flask_cors


# Ejecucion
## Instalacion de bot en telegram
1. Accede a la plataforma de mensajería Telegram.
2. Realiza una búsqueda en Telegram del bot llamado "DSGTestBot".
3. Ejecuta la interfaz de programación de aplicaciones (API REST) correspondiente.
4. Inicia el bot o envía un mensaje para que el usuario se registre automáticamente en la base de datos y pueda recibir mensajes.
![Image text](https://github.com/diegosg15/dsg_test_bot_telegram/blob/main/assets/bot.jpeg)
![Image text](https://github.com/diegosg15/dsg_test_bot_telegram/blob/main/assets/chatBot.jpeg)

## Ejecución APIREST en Windows

Sigue las instrucciones a continuación para ejecutar el código en Windows:
1. Clona el repositorio en tu máquina local.
2. Abre una ventana de terminal o símbolo del sistema.
3. Navega hasta el directorio raíz del proyecto.
4. Crea y activa un entorno virtual para el proyecto (se recomienda, pero opcional).
5. Instala las dependencias del proyecto ejecutando el siguiente comando:
```bash
pip install -r requirements.txt
```
6. Dentro de la carpeta "app", ejecuta el siguiente comando:
```bash
python app.py
```

## Ejecución APIREST en Ubuntu (Produccion)
1. Actualizar el sistema operativo Ubuntu:
```bash
sudo apt-get update
```

2. Instalar pip en caso de no tenerlo instalado:
```bash
sudo apt install python3-pip
```

3. Instalar virtualenv con pip:
```bash
pip3 install virtualenv
```

4. Instalar python3-virtualenv y python3-venv con apt:
```bash
sudo apt install python3-virtualenv python3-venv
```

5. Crear un directorio en /var/www/ para el proyecto:
```bash
sudo mkdir /var/www/
```

6. clonar el proyecto en /var/www/
```bash
cd /var/www/
sudo git clone https://github.com/diegosg15/dsg_test_bot_telegram.git
```


7. Dar permisos al proyecto para el usuario del servidor:
Reemplazar "userName" con el nombre de usuario del servidor
```bash
sudo chown -R ubuntu:ubuntu /var/www/dsg_test_bot_telegram 
```

8. Establecer permisos adecuados para el proyecto:
```bash
sudo chmod 755 /var/www/dsg_test_bot_telegram
```

9. Navegar al directorio del proyecto:
```bash
cd /var/www/dsg_test_bot_telegram
```

10. Crear un entorno virtual de Python:
```bash
python3 -m venv dsgtestbotenv
```

11. Activar el entorno virtual
```bash
source dsgtestbotenv/bin/activate
```

12. Instalar las dependencias del proyecto desde el archivo requirements.txt:
```bash
pip3 install -r requirements.txt
```

13. Navegar al directorio "app/"
```bash
cd app/
```

14. Probar el servicio con el siguiente comando de gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 entrypoint:appFlask
#Detener la prueba presionando Ctrl + C.
```

15. Editar el archivo "DSGTestBot.service" usando un editor de texto como "nano":
```bash
nano ./DSGTestBot.service
```

16. Editar el usuario en la sección [Service] con el nombre de usuario del servidor:
```bash
[Service]
User=ubuntu Reemplazar "ubuntu" con el nombre de usuario del servidor
```

17. Copiar el archivo de servicio al directorio /etc/systemd/system/:
```bash
sudo cp DSGTestBot.service /etc/systemd/system/
```

18. Iniciar el servicio
```bash
sudo systemctl start DSGTestBot
```

19. Habilitar el servicio para que se inicie automáticamente al reiniciar el servidor:
```bash
sudo systemctl start DSGTestBot
```

20. Verificar el estado del servicio:
```bash
sudo systemctl status DSGTestBot
```

21. Reiniciar el servidor Ubuntu para aplicar los cambios:
```bash
sudo reboot
```

## Pruebas Unitarias
El código incluye pruebas unitarias para algunas funcionalidades. Para ejecutar las pruebas, sigue estos pasos:

- Asegúrate de haber realizado la configuración necesaria como se mencionó anteriormente.
- Dentro de la carpeta app ejecuta: pytest

Las pruebas verificarán el correcto funcionamiento de las operaciones de envío y recepción de mensajes.


## Request API REST

### Obtener mensajes [GET]
- URL: `http://localhost:5000/v0/messages`
- Método: GET
- Descripción: Esta petición obtiene todos los mensajes almacenados en la base de datos organizados por usuario.
- Respuesta exitosa:

```bash
GET /v0/messages
{
  "data": [
    {
      "id": "user1",
      "first_name": "John",
      "last_name": "Doe",
      "messages": [
        {
          "text": "Hola",
          "date": "2023-06-10 10:00:00"
        },
        {
          "text": "Adiós",
          "date": "2023-06-10 11:00:00"
        }
      ]
    },
    {
      "id": "user2",
      "first_name": "Jane",
      "last_name": "Smith",
      "messages": [
        {
          "text": "Saludos",
          "date": "2023-06-10 12:00:00"
        }
      ]
    }
  ]
}
```

### Enviar mensaje (POST)

- URL: `http://localhost:5000/v0/messages`
- Método: POST
- Descripción: Esta petición permite enviar un mensaje a todos los usuarios registrados o a un usuario específico por su ID.
- Parámetros de entrada:
    - `id` (opcional): ID del usuario al que se desea enviar el mensaje.
    - `message`: Mensaje a enviar.
- Peticiones Ejemplos:
    - Envio de mensaje a un usuario especifico
      ```bash
      POST /v0/messages

      {
        "id": "user1",
        "message": "Hola usuario user1"
      }
      ```

    - Envio de mensaje a todos los usuarios registrados.
      ```bash
      POST /v0/message
      {
        "message": "Hola a todos"
      }
      ```
- Respuesta exitosa:
    - Código de estado: 200
    - Cuerpo de respuesta: 
        ```json
        {
            "status": "message sent to user"
        }
        ```
        ```json
        {
            "status": "message sent to all users"
        }
        ```
































