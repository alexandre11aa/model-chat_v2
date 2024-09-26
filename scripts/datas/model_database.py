from consumer.models import CustomUser

# Crie um superuser
superuser = CustomUser.objects.create_superuser(
    name='admin',
    email='admin@example.com',
    password='admin',
    matricula=1000,
    sexo='M'
)

# Crie outros usuários
user1 = CustomUser.objects.create_user(
    name='Joao',
    email='joao@example.com',
    password='senha123',
    matricula=1001,
    sexo='M'
)

user2 = CustomUser.objects.create_user(
    name='Maria',
    email='maria@example.com',
    password='senha123',
    matricula=1002,
    sexo='F'
)

user3 = CustomUser.objects.create_user(
    name='Pedro',
    email='pedro@example.com',
    password='senha123',
    matricula=1003,
    sexo='O'
)

user4 = CustomUser.objects.create_user(
    name='Ana',
    email='ana@example.com',
    password='senha123',
    matricula=1004,
    sexo='N'
)

exit()