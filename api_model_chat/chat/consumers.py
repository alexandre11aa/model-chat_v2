import json
from channels.generic.websocket import AsyncWebsocketConsumer

def get_room_name(user1_code, user2_code):
    return f"chat_{min(user1_code, user2_code)}_{max(user1_code, user2_code)}"

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtenha os códigos dos usuários a partir da URL
        self.user_code = self.scope['url_route']['kwargs'].get('user1_code')
        self.target_code = self.scope['url_route']['kwargs'].get('user2_code')
        
        if not self.user_code or not self.target_code:
            # Código de usuário não encontrado
            await self.close()
            return
        
        self.room_name = get_room_name(self.user_code, self.target_code)

        # Adiciona o WebSocket ao grupo do chat
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove o WebSocket do grupo do chat
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # Envia a mensagem para o grupo do chat
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'send_message',
                'message': message,
                'username': username
            }
        )

    async def send_message(self, event):
        message = event['message']
        username = event['username']

        # Envia a mensagem para o WebSocket do cliente
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))