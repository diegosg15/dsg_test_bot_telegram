import unittest 
import time
from flask import Flask
from pymongo import MongoClient
from telegram import Bot
from unittest import mock
from unittest.mock import patch, MagicMock
from app.app import appFlask, send_message, get_index_by_id, receive_message, get_messages, change_db_test
import asyncio

class TestYourCode(unittest.TestCase):

    def setUp(self):
        # Crear una instancia de Flask para las pruebas
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.add_url_rule('/v0/messages', 'receive_message',receive_message, methods=['POST'])
        self.app.add_url_rule('/v0/messages', 'get_messages', lambda: get_messages(), methods=['GET'])
        self.maxDiff = None
        self.client = self.app.test_client()
        
        # Configurar la colección de mensajes con datos de prueba
        self.collectionMessage = change_db_test()
        self.collectionMessage.delete_many({})  # Elimina todos los documentos en la colección
        self.collectionMessage.insert_one({'id': '12345', 'first_name': 'x', 'last_name': 'x', 'text': 'usuario 12345 mensaje 1', 'date': '2023-06-11'})
        self.collectionMessage.insert_one({'id': '12345', 'first_name': 'x', 'last_name': 'x', 'text': 'usuario 12345 mensaje 2', 'date': '2023-06-11'})
        self.collectionMessage.insert_one({'id': '123', 'first_name': 'y', 'last_name': 'y', 'text': 'usuario 123 mensaje 1', 'date': '2023-06-11'})
        self.collectionMessage.insert_one({'id': '123', 'first_name': 'y', 'last_name': 'y', 'text': 'usuario 123 mensaje 2', 'date': '2023-06-11'})


    def tearDown(self):
        # Eliminar los datos de la base de datos o colección de mensajes
        self.collectionMessage.delete_many({})  # Elimina todos los documentos en la colección
        # Detener los parches
        patch.stopall()


    def test_get_index_by_id(self):
        # Prueba de la función get_index_by_id
        # Creamos una lista de diccionarios de prueba y verificamos que el índice se obtenga correctamente
        data = [
            {'id': '1', 'name': 'John'},
            {'id': '2', 'name': 'Jane'},
            {'id': '3', 'name': 'Alice'}
        ]
        self.assertEqual(get_index_by_id(data, '2'), 1)
        self.assertEqual(get_index_by_id(data, '4'), -1)

    def test_get_messages(self):
        # Prueba del endpoint /v0/messages con el método GET
        # Simulamos una solicitud GET y verificamos la respuesta
        
        response = self.client.get('/v0/messages')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'data': [
                    {'first_name': 'x',
                    'id': '12345',
                    'last_name': 'x',
                    'messages': [{'date': '2023-06-11',
                                    'text': 'usuario 12345 mensaje 1'},
                                    {'date': '2023-06-11',
                                    'text': 'usuario 12345 mensaje 2'}]},
                  {'first_name': 'y',
                    'id': '123',
                    'last_name': 'y',
                    'messages': [{'date': '2023-06-11', 'text': 'usuario 123 mensaje 1'},
                                {'date': '2023-06-11', 'text': 'usuario 123 mensaje 2'}]}]
                })

    @mock.patch('app.app.send_message_async')  # Mock la función send_message_async
    def test_receive_message_with_id(self, mock_response):
        # Prueba del endpoint /v0/messages con el método POST
        # Simulamos una solicitud POST con datos de prueba y verificamos la respuesta
        mock_response.return_value  = None
        response = self.client.post('/v0/messages', data={'id': 'user123', 'message': 'Hello'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'message sent to user'})



    @mock.patch('app.app.send_message_async')  # Mock la función send_message_async
    def test_receive_message_without_id(self, mock_response):
        # Prueba del endpoint /v0/messages con el método POST
        # Simulamos una solicitud POST con datos de prueba y verificamos la respuesta
        mock_response.return_value  = None
        response = self.client.post('/v0/messages', data={'message': 'Hello'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'message sent to all users'})
if __name__ == '__main__':
    unittest.main()

               
