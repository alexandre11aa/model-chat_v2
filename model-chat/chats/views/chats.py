from rest_framework.response import Response

from django.db.models import Q
from django.utils.timezone import now

from chats.views.base import BaseView
from chats.models import Chat
from chats.serializers import ChatSerializer

from core.socket import socket


class ChatsView(BaseView):
    def get(self, request):
        chats = Chat.objects.filter(
            Q(from_user_id=request.user.id) | Q(to_user_id=request.user.id),
            deleted_at__isnull=True
        ).order_by('-viewed_at').all()

        serializer = ChatSerializer(
            chats,
            context={'user_id': request.user.id},
            many=True
        )

        return Response({
            'chats': serializer.data
        })
    
    def post(self, request):
        email = request.data.get('email')

        # Getting user
        user = self.get_user(email=email)

        # Check if chat already exists
        chat = self.has_existing_chat(user_id=request.user.id, to_user=user.id)

        # Creating chat
        if not chat:
            chat = Chat.objects.create(
                from_user=request.user,
                to_user=user,
                viewed_at=now()
            )

            chat = ChatSerializer(
                chat,
                context={'user_id': request.user.id},
            ).data

            # Sending chat to user
            socket.emit('update_chat', {
                'query': {
                    'users': [request.user.id, user.id]
                }
            })

        return Response({
            'chat': chat
        })
    

class ChatView(BaseView):
    def delete(self, request, chat_id):
        # Checking if chat belongs to user
        chat = self.chat_belongs_to_user(
            user_id=request.user.id,
            chat_id=chat_id
        )

        # Deleting chat
        deleted = Chat.objects.filter(
            id=chat_id,
            deleted_at__isnull=True
        ).update(deleted_at=now())

        if deleted:
            # Sending update chat to users
            socket.emit('update_chat', {
                'type': 'delete',
                'query': {
                    'chat_id': chat_id,
                    'users': [chat.from_user_id, chat.to_user_id]
                }
            })

        return Response({
            'success': True
        })