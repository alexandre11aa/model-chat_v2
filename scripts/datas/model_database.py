from consumer.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist

def create_user_if_not_exists(name, email, password, matricula, sexo, user):

    # Tenta obter o usuário pelo número de matrícula
    try:    
        existing_user = CustomUser.objects.get(matricula=matricula)
        return existing_user
    
    # Se não existir, cria um novo usuário ou super-usuário    
    except ObjectDoesNotExist:

        if user == 's':
            tipo_de_usuario = CustomUser.objects.create_superuser
            
        elif user == 'u':
            tipo_de_usuario = CustomUser.objects.create_user
        
        return tipo_de_usuario(
                name=name,
                email=email,
                password=password,
                matricula=matricula,
                sexo=sexo
            )

# Crie um superuser
superuser = create_user_if_not_exists(
    name='admin',
    email='admin@example.com',
    password='admin',
    matricula=1000,
    sexo='M',
    user='s'
)

# Crie outros usuários
user1 = create_user_if_not_exists(
    name='Joao',
    email='joao@example.com',
    password='senha123',
    matricula=1001,
    sexo='M',
    user='u'
)

user2 = create_user_if_not_exists(
    name='Maria',
    email='maria@example.com',
    password='senha123',
    matricula=1002,
    sexo='F',
    user='u'
)

user3 = create_user_if_not_exists(
    name='Pedro',
    email='pedro@example.com',
    password='senha123',
    matricula=1003,
    sexo='O',
    user='u'
)

user4 = create_user_if_not_exists(
    name='Ana',
    email='ana@example.com',
    password='senha123',
    matricula=1004,
    sexo='N',
    user='u'
)

exit()
