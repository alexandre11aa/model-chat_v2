import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from consumer.models import CustomUser
from .models import DuoMessage, DuoFile
from channels.db import database_sync_to_async

# Função que define o nome da sala de chat baseada nos códigos dos dois usuários
def get_room_name(user1_code, user2_code):
    return f"chat_{min(user1_code, user2_code)}_{max(user1_code, user2_code)}"  
    # O nome da sala é gerado com base nos códigos dos usuários. O menor código vem primeiro para garantir que a sala seja sempre a mesma independentemente da ordem.

# Classe que gerencia a conexão WebSocket do chat
class ChatConsumer(AsyncWebsocketConsumer):

    # Método chamado quando o WebSocket é aberto (cliente se conecta)
    async def connect(self):
        print('\nIniciando processamento assíncrono:\n')

        # Obtém o código do usuário e do alvo (a outra pessoa no chat) a partir da URL
        self.user_code = self.scope['url_route']['kwargs'].get('user1_code')
        self.target_code = self.scope['url_route']['kwargs'].get('user2_code')
        
        # Se um dos códigos estiver faltando, fecha a conexão
        if not self.user_code or not self.target_code:
            print(f"Conexão fechada: user_code ou target_code ausente. user_code: {self.user_code}, target_code: {self.target_code}\n")
            await self.close()
            return
        
        # Define o nome da sala de chat com base nos códigos dos usuários
        self.room_name = get_room_name(self.user_code, self.target_code)
        print(f"Conectando na sala: {self.room_name}")

        # Adiciona o canal do cliente ao grupo de WebSocket (sala de chat)
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        
        await self.accept()  # Aceita a conexão WebSocket
        print(f"Conexão aceita para user_code: {self.user_code}")

    # Método chamado quando o WebSocket é desconectado
    async def disconnect(self, close_code):
        # Remove o canal do cliente do grupo de WebSocket (sala de chat)
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
        print(f"Conexão fechada: {self.user_code} desconectado.")

    # Método chamado quando o servidor recebe uma mensagem do WebSocket
    async def receive(self, text_data):
        data_json = json.loads(text_data)

        # Verifica se é uma mensagem de texto ou arquivo
        message = data_json.get('message', None)
        file = data_json.get('file', None)  # Verifica se há um arquivo

        sender = await database_sync_to_async(CustomUser.objects.get)(code=self.user_code)
        receiver = await database_sync_to_async(CustomUser.objects.get)(code=self.target_code)

        if message:  # Caso seja uma mensagem de texto
            await database_sync_to_async(DuoMessage.objects.create)(
                sender=sender,
                receiver=receiver,
                message=message
            )

            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'send_message',
                    'message': message,
                    'username': sender.name,
                    'time': datetime.now().strftime("%H:%M")
                }
            )

        elif file:  # Caso seja um arquivo
            pass # Escreva uma lógica similar ao de mensagem, para file

    # Método chamado quando uma mensagem é enviada para o grupo (sala de chat)
    async def send_message(self, event):
        message = event['message']  # Obtém a mensagem do evento
        username = event['username']  # Obtém o nome do usuário que enviou a mensagem
        time = event['time']  # Obtém o timestamp da mensagem

        # Envia a mensagem de volta para o cliente WebSocket no formato JSON
        await self.send(text_data=json.dumps({
            'message': message,  # Envia o texto da mensagem
            'username': username,  # Envia o nome do remetente
            'time': time  # Envia o timestamp
        }))
        print(f"Mensagem enviada ao cliente: {message} de {username} às {time}")

        print('\nFinalizando processamento assíncrono.\n')

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_code = self.scope['url_route']['kwargs']['user_code']
        self.group_name = f"user_notifications_{self.user_code}"
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notify(self, event):
        await self.send(text_data=json.dumps({
            'from_user': event['from_user']
        }))