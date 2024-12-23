from core.socket import socket
from core.utils.exceptions import ValidationError

from chats.views.base import BaseView
from chats.models import Chat, ChatMessage
from chats.serializers import ChatMessagesSerializer

from attachments.models import FileAttachment, AudioAttachment

from rest_framework.response import Response

from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import uuid


class ChatMessagesView(BaseView):
    def get(self, request, chat_id):
        # Checking if chat belongs to user
        chat = self.chat_belongs_to_user(
            user_id=request.user.id,
            chat_id=chat_id
        )

        # Marking messages as seen
        self.mark_messages_as_seen(chat_id, request.user.id)

        # Update all chat messages as seen
        socket.emit('mark_messages_as_seen', {
            'query':{
                'chat_id': chat_id,
                'exclude_user_id': request.user.id
            }
        })

        # Getting chat messages
        messages = ChatMessage.objects.filter(
            chat_id=chat_id,
            deleted_at__isnull=True
        ).order_by('created_at').all()

        serializer = ChatMessagesSerializer(messages, many=True)

        # Sending update chat to users
        socket.emit('update_chat', {
            'query': {
                'users': [chat.from_user_id, chat.to_user_id]
            }
        })

        return Response({
            'messages': serializer.data
        })
    
    def post(self, request, chat_id):
        body = request.data.get('body')
        file = request.FILES.get('file')
        audio = request.FILES.get('audio')

        # Checking if chat belongs to user
        chat = self.chat_belongs_to_user(
            user_id=request.user.id,
            chat_id=chat_id
        )

        # Marking messages as seen
        self.mark_messages_as_seen(chat_id, request.user.id)

        # Validating request params
        if not body and not file and not audio:
            raise ValidationError('Nenhum parâmetro foi informado!')
        
        attachment = None

        if file:
            storage = FileSystemStorage(
                settings.MEDIA_ROOT / 'files',
                settings.MEDIA_URL + 'files'
            )

            content_type = file.content_type
            name = file.name.split('.')[0]  # arquivo.py -> 'arquivo'
            extension = file.name.split('.')[-1]  # arquivo.py -> 'py'
            size = file.size

            # Validation file sizer:
            if size > 100000000:
                raise ValidationError('O arquivo deve ter no máximo 100 mb!')
            
            # Upload new file
            file = storage.save(f'{uuid.uuid4()}.{extension}', file)
            src = storage.url(file)

            # Save new attachment
            attachment = FileAttachment.objects.create(
                name=name,
                extension=extension,
                size=size,
                src=src,
                content_type=content_type
            )

        if audio:
            storage = FileSystemStorage(
                settings.MEDIA_ROOT / 'audios',
                settings.MEDIA_URL + 'audios'
            )

            # Upload new audio
            audio = storage.save(f'{uuid.uuid4()}.mp3', audio)
            src = storage.url(audio)

            # Save new attachment
            attachment = AudioAttachment.objects.create(
                src=src
            )

        # Saving message
        chat_message = ChatMessage.objects.create(
            chat_id=chat_id,
            body=body,
            from_user_id=request.user.id,
            attachment_code='FILE' if file else 'AUDIO' if audio else None,
            attachment_id=attachment.id if attachment else None
        )

        chat_message_data = ChatMessagesSerializer(chat_message).data

        # Emitting new messages to chat
        socket.emit('update_chat_message', {
            'type': 'create',
            'message': chat_message_data,
            'query': {
                'chat_id': chat_id
            }
        })

        # Updating chat viewed_at
        Chat.objects.filter(id=chat_id).update(viewed_at=now())

        # Sending update chat to users
        socket.emit('update_chat', {
            'query': {
                'users': [chat.from_user_id, chat.to_user_id]
            }
        })

        return Response({
            'messages': chat_message_data
        })


class ChatMessageView(BaseView):
    def delete(self, request, chat_id, message_id):
        # Checking if chat belongs to user
        chat = self.chat_belongs_to_user(
            user_id=request.user.id,
            chat_id=chat_id
        )

        # Deleting message
        deleted = ChatMessage.objects.filter(
            id=message_id,
            chat_id=chat_id,
            from_user_id=request.user.id,
            deleted_at__isnull=True
        ).update(deleted_at=now())

        if deleted:
            # Emitting update chat message
            socket.emit('update_chat_message', {
                'type': 'delete',
                'query': {
                    'chat_id': chat_id,
                    'message_id': message_id
                }
            })

            # Sending update chat to users
            socket.emit('update_chat', {
                'query': {
                    'users': [chat.from_user_id, chat.to_user_id]
                }
            })

        return Response({
            'success': True
        })