import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from consumer.models import CustomUser  # Certifique-se de que o caminho está correto
from .models import Message  # Certifique-se de que o modelo Message está correto
from channels.db import database_sync_to_async

def get_room_name(user1_code, user2_code):
    return f"chat_{min(user1_code, user2_code)}_{max(user1_code, user2_code)}"

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_code = self.scope['url_route']['kwargs'].get('user1_code')
        self.target_code = self.scope['url_route']['kwargs'].get('user2_code')
        
        if not self.user_code or not self.target_code:
            await self.close()
            return
        
        self.room_name = get_room_name(self.user_code, self.target_code)

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username_code = text_data_json['username']

        print(f"Mensagem recebida: {message} de {username_code}")  # Debug

        # Obtenha o remetente (sender) e o destinatário (receiver)
        try:
            sender = await database_sync_to_async(CustomUser.objects.get)(code=self.user_code)
            receiver = await database_sync_to_async(CustomUser.objects.get)(code=self.target_code)
            
            print(f"Salvando mensagem de {sender} para {receiver}")  # Debug

            # Salvar a mensagem no banco de dados
            await database_sync_to_async(Message.objects.create)(
                sender=sender,
                receiver=receiver,
                message=message
            )
            
            print("Mensagem salva com sucesso!")  # Debug

        except CustomUser.DoesNotExist:
            print(f"Usuário não encontrado: {self.user_code} ou {self.target_code}")
            return

        # Envia a mensagem para o grupo do chat
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'send_message',
                'message': message,
                'username': sender.name,  # Usar o nome do usuário
                'time': datetime.now().strftime("%H:%M")  # Adiciona o timestamp
            }
        )

    async def send_message(self, event):
        message = event['message']
        username = event['username']
        time = event['time']  # Recebe o timestamp

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'time': time  # Envia o timestamp
        }))