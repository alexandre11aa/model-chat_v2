import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from consumer.models import CustomUser
from .models import Message
from channels.db import database_sync_to_async

# Função que define o nome da sala de chat baseada nos códigos dos dois usuários
def get_room_name(user1_code, user2_code):
    return f"chat_{min(user1_code, user2_code)}_{max(user1_code, user2_code)}"  
    # O nome da sala é gerado com base nos códigos dos usuários. O menor código vem primeiro para garantir que a sala seja sempre a mesma independentemente da ordem.

# Classe que gerencia a conexão WebSocket do chat
class ChatConsumer(AsyncWebsocketConsumer):

    # Método chamado quando o WebSocket é aberto (cliente se conecta)
    async def connect(self):

        # Obtém o código do usuário e do alvo (a outra pessoa no chat) a partir da URL
        self.user_code = self.scope['url_route']['kwargs'].get('user1_code')
        self.target_code = self.scope['url_route']['kwargs'].get('user2_code')
        
        # Se um dos códigos estiver faltando, fecha a conexão
        if not self.user_code or not self.target_code:
            await self.close()
            return
        
        # Define o nome da sala de chat com base nos códigos dos usuários
        self.room_name = get_room_name(self.user_code, self.target_code)

        # Adiciona o canal do cliente ao grupo de WebSocket (sala de chat)
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        
        await self.accept()  # Aceita a conexão WebSocket

    # Método chamado quando o WebSocket é desconectado
    async def disconnect(self, close_code):

        # Remove o canal do cliente do grupo de WebSocket (sala de chat)
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    # Método chamado quando o servidor recebe uma mensagem do WebSocket
    async def receive(self, text_data):

        # Converte os dados JSON recebidos em um dicionário
        text_data_json = json.loads(text_data)
        message = text_data_json['message']  # Extrai a mensagem do dicionário
        username_code = text_data_json['username']  # Extrai o código do usuário que enviou a mensagem

        print(f"Mensagem recebida: {message} de {username_code}")  # Debug para verificar a mensagem recebida

        # Obtém o remetente (sender) e o destinatário (receiver) das mensagens
        try:
            # Busca o objeto do usuário remetente no banco de dados de forma assíncrona
            sender = await database_sync_to_async(CustomUser.objects.get)(code=self.user_code)
            # Busca o objeto do usuário destinatário no banco de dados de forma assíncrona
            receiver = await database_sync_to_async(CustomUser.objects.get)(code=self.target_code)
            
            print(f"Salvando mensagem de {sender} para {receiver}")  # Debug para indicar que a mensagem será salva

            # Salva a mensagem no banco de dados de forma assíncrona
            await database_sync_to_async(Message.objects.create)(
                sender=sender,
                receiver=receiver,
                message=message
            )
            
            print("Mensagem salva com sucesso!")  # Debug para indicar que a mensagem foi salva

        # Caso um dos usuários não seja encontrado, exibe um erro no console
        except CustomUser.DoesNotExist:
            print(f"Usuário não encontrado: {self.user_code} ou {self.target_code}")
            return

        # Envia a mensagem para todos os membros do grupo (sala de chat)
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'send_message',  # Especifica o tipo de evento a ser tratado
                'message': message,  # Inclui a mensagem enviada
                'username': sender.name,  # Inclui o nome do remetente
                'time': datetime.now().strftime("%H:%M")  # Adiciona o timestamp (hora atual)
            }
        )

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