from rest_framework.exceptions import APIException


class UserNotFound(APIException):
    status_code = 404
    default_detail = 'Usuário não encontrado!'
    default_code = 'user_not_found'


class ChatNotFound(APIException):
    status_code = 404
    default_detail = 'Chat não encontrado e/ou não pertence ao usuário!'
    default_code = 'chat_not_found'