"""
Nombre de la Aplicación: DSGTestBot
Versión: 0.0
Desarrollador: Diego Salgado Giles
Fecha de creacion: 10/06/2023
Descripcion: Este API permite enviar mensajes a usuarios registrados en una base de datos MongoDB a través de Telegram. 
Los usuarios se registran automáticamente al enviar un mensaje al bot. 
Se almacenan los mensajes en la base de datos y se ofrecen dos peticiones: 
una GET para obtener mensajes organizados por usuario 
y una POST para enviar mensajes a todos los usuarios o a uno específico por ID.
"""

#Librerias
import asyncio
import threading
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from bson.json_util import dumps
from unittest.mock import patch, MagicMock

#intanciando flask
appFlask = Flask(__name__)
CORS(appFlask)

client = MongoClient('localhost', 27017)
db = client['DSGTestBot']
collectionUser    = db['user']                               #collecion donde se alamacenan los usuario
collectionMessage = db['message']                            #collecion donde se alamcenan los mensajes recibidos

# Seleccionando las colección
tokenBot = "6016652364:AAGaqDZWSvsUF-Zk1zuMN3yv1tl066cdgoc"  #token del bot de telegram


''''''''''''''''''''''EndPoints '''''''''''
@appFlask.route('/v0/messages', methods=['GET'])
def get_messages():
    data = []
    # Obtener todos los mensajes de la colección
    for message in collectionMessage.find():
        # Buscar el índice del usuario en la lista de datos
        index = get_index_by_id(data, message["id"])

        # Extraer los campos relevantes del mensaje
        message_data = {
            "text": message["text"],
            "date": message["date"]
        }

        # Verificar si es necesario agregar un nuevo usuario a la lista de datos
        if index == -1:
            user_data = {
                "id": message["id"],
                "first_name": message["first_name"],
                "last_name": message["last_name"],
                "messages": [message_data]
            }
            data.append(user_data)
        else:
            # Agregar el mensaje al usuario existente en la lista de datos
            data[index]['messages'].append(message_data)

    return jsonify({'data': data})


@appFlask.route('/v0/messages', methods=['POST'])
def receive_message():
    data = request.form
    # Verificar si se proporciona un ID específico en los datos recibidos
    if 'id' in data:
        send_message_async(data['id'], data['message'])
        return jsonify({'status': "message sent to user"})
    else:
        # Enviar el mensaje a todos los usuarios en la colección
        for user in collectionUser.find():
            send_message_async(user['id'], data['message'])
        return jsonify({'status': 'message sent to all users'})

    


# Obtener el índice de un elemento en una lista de diccionarios por su "id"
def get_index_by_id(arr, id):
    try:
        # Utilizar una expresión generadora para encontrar el índice
        index = next(index for (index, d) in enumerate(arr) if d["id"] == id)
        return index
    except StopIteration:
        return -1  # Si no se encuentra el documento con el id dado, se devuelve -1



# Función para iniciar el bot de Telegram
async def start_telegram_bot():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sendMessage())# Esperar a que send_message se complete


def send_message_async(id,message):
    asyncio.run(send_message(id, message))

# Enviar un mensaje usando la API de Telegram
async def send_message(id, message):
    global tokenBot 
    bot = Bot(token=tokenBot)
    await bot.send_message(chat_id=id, text=message)


#Funcion para cambiar la base de datos para las pruebas unitarias
def  change_db_test():
    global db, collectionMessage, collectionUser
    db = client['DSGTestBotTest']
    collectionUser    = db['user']                               #collecion donde se alamacenan los usuario
    collectionMessage = db['message']                            #collecion donde se alamcenan los mensajes recibidos
    return collectionMessage


# Función para ejecutar el bot de Telegram
def run_telegram_bot(tokenBot):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def handlerMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
        res = collectionUser.find_one({'id': update.message.chat.id}) 
        if(res == None):
            docUser={
                "id": update.message.chat.id,
                "first_name":update.message.chat.first_name,
                "last_name":update.message.chat.last_name
            }
            collectionUser.insert_one(docUser)
        docMessage={
                "id": update.message.chat.id,
                "first_name":update.message.chat.first_name,
                "last_name":update.message.chat.last_name,
                "date":update.message.date,
                "text": update.message.text,
                "mesage_id": update.message.message_id
            }
        collectionMessage.insert_one(docMessage)

    app = ApplicationBuilder().token(tokenBot).build()
    app.add_handler(MessageHandler(None, handlerMessage))
    app.run_polling()

# Iniciar la aplicación Flask
def run_flask_app():
    appFlask.run(host='0.0.0.0')

# Función principal
if __name__ == '__main__':
    # Crear los hilos para ejecutar flask y telegram del código
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    telegram_thread = threading.Thread(target=run_telegram_bot(tokenBot))
    telegram_thread.start()
    
    telegram_thread.join()
    flask_thread.join()