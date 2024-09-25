import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import GroupChat, GroupMessage
from consumer.models import CustomUser

# Classe que lida com o WebSocket para o chat em grupo
class GroupChatConsumer(AsyncWebsocketConsumer):
    
    # Método assíncrono que é chamado quando o WebSocket é conectado
    async def connect(self):

        # Obtém o ID do chat de grupo a partir da URL
        self.group_chat_id = self.scope['url_route']['kwargs']['group_chat_id']
        
        # Cria um nome único para o chat em grupo
        self.group_chat_name = f'group_{self.group_chat_id}'

        # Adiciona o canal do consumidor ao grupo de canais do chat em grupo
        await self.channel_layer.group_add(
            self.group_chat_name,
            self.channel_name
        )

        # Aceita a conexão WebSocket
        await self.accept()

    # Método assíncrono que é chamado quando o WebSocket é desconectado
    async def disconnect(self, close_code):

        # Remove o canal do consumidor do grupo de canais do chat em grupo
        await self.channel_layer.group_discard(
            self.group_chat_name,
            self.channel_name
        )

    # Método que lida com a recepção de mensagens via WebSocket
    async def receive(self, text_data):

        # Converte os dados recebidos em JSON
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']

        # Salva a mensagem no banco de dados
        sender = await self.get_user(sender_id)  # Obtém o usuário que enviou a mensagem
        group_chat = await self.get_group_chat(self.group_chat_id)  # Obtém o chat em grupo
        group_message = await self.create_group_message(group_chat, sender, message)  # Cria a mensagem no banco de dados

        # Envia a mensagem para todos os membros do grupo
        await self.channel_layer.group_send(
            self.group_chat_name,
            {
                'type': 'chat_message',  # Define o tipo de evento como 'chat_message'
                'message': {
                    'sender': sender.name,  # Nome do remetente
                    'message': group_message.message,  # Texto da mensagem
                    'timestamp': group_message.timestamp.isoformat()  # Timestamp da mensagem no formato ISO
                }
            }
        )

    # Método que lida com o evento de envio de mensagem
    async def chat_message(self, event):
        message = event['message']

        # Envia a mensagem de volta ao WebSocket em formato JSON
        await self.send(text_data=json.dumps({
            'message': message
        }))

    # Método para obter o usuário de forma assíncrona a partir do banco de dados
    @database_sync_to_async
    def get_user(self, user_id):

        # Retorna o usuário com o ID fornecido
        return CustomUser.objects.get(id=user_id)

    # Método para obter o chat em grupo de forma assíncrona a partir do banco de dados
    @database_sync_to_async
    def get_group_chat(self, group_chat_id):

        # Retorna o chat em grupo com o ID fornecido
        return GroupChat.objects.get(id=group_chat_id)

    # Método para criar uma nova mensagem no chat de grupo de forma assíncrona
    @database_sync_to_async
    def create_group_message(self, group_chat, sender, message):

        # Cria e retorna uma nova mensagem associada ao chat e remetente
        return GroupMessage.objects.create(
            group_chat=group_chat,
            sender=sender,
            message=message
        )