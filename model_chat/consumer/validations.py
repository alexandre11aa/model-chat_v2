from django.core.exceptions import ValidationError

from .models import CustomUser
    
def email_unique(value, instance=None):

    # Se estiver atualizando, permite o uso do email atual do colaborador
    existing_colaborador = CustomUser.objects.filter(email=value).exclude(id=instance.id if instance else None)

    if existing_colaborador.exists():
        raise ValidationError('Este email já está em uso. Por favor, escolha outro.')
     
def remove_dot_hyphen_parentheses_espace_formatting(value):
    
    # Converte o valor para string, caso não seja
    if not isinstance(value, str):
        value = str(value)
    
    # Remove os caracteres indesejados
    number_unformatted = value.replace(".", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
    
    return number_unformatted