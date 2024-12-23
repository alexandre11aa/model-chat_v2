from rest_framework.exceptions import APIException

class ValidationError(APIException):
    status_code = 400
    default_detail = 'Parâmetros inválidos para a requisição!'
    default_code = 'validation_error'