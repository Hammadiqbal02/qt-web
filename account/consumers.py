import json
import aiohttp
from rest_framework_simplejwt.tokens import AccessToken
from channels.generic.websocket import AsyncWebsocketConsumer

connections = {}


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def get_user_id_from_token(self, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            return user_id
        except Exception as e:
            # Handle invalid token
            raise Exception('Error: {e}')

    async def receive(self, text_data):
        global connections
        text_data_json = json.loads(text_data)
        if 'machine_name' in text_data_json:
            bearer_token = text_data_json.get('token')
            user_id = await self.get_user_id_from_token(bearer_token)
            connections[user_id] = self
            del text_data_json['token']
            headers = {'Authorization': f'Bearer {bearer_token}'} if bearer_token else {}
            async with aiohttp.ClientSession() as session:
                async with session.post('http://127.0.0.1:8000/api/user/user-connection/', data=text_data_json,
                                        headers=headers) as resp:
                    # Do something with the response, like sending it back to the WebSocket client
                    response = {'message': 'user connection created successfully'}
                    # send message to client
                    await connections[user_id].send(json.dumps(response))

        elif 'wavelength' in text_data_json:
            print("wavelength")
            bearer_token = text_data_json.get('token')
            user_id = await self.get_user_id_from_token(bearer_token)
            del text_data_json['token']
            headers = {'Authorization': f'Bearer {bearer_token}'} if bearer_token else {}
            async with aiohttp.ClientSession() as session:
                async with session.post('http://127.0.0.1:8000/api/user/scan-data/', data=text_data_json,
                                        headers=headers) as resp:
                    # Do something with the response, like sending it back to the WebSocket client
                    response = {'message': 'data scanned successfully'}
                    # send message to server
                    await connections[user_id].send(json.dumps(response))

        elif 'is_connection_alive' in text_data_json:
            bearer_token = text_data_json.get('token')
            user_id = await self.get_user_id_from_token(bearer_token)
            del text_data_json['token']
            headers = {'Authorization': f'Bearer {bearer_token}'} if bearer_token else {}
            async with aiohttp.ClientSession() as session:
                async with session.put('http://127.0.0.1:8000/api/user/user-connection/', data=text_data_json,
                                       headers=headers) as resp:
                    # Do something with the response, like sending it back to the WebSocket client
                    response = {'message': 'user connection updated successfully'}
                    # send message to server
                    await connections[user_id].send(json.dumps(response))
        elif 'is_scan_data' in text_data_json:
            if text_data_json['is_scan_data'] == 'yes':
                user_id = text_data_json['user_id']
                print(user_id)
                print(connections[user_id])
                await self.send(json.dumps(text_data_json))
