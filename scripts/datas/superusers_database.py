import os
import django

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ramal_unifip.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_superuser_if_not_exists(username, email, password):
    User = get_user_model()  # Utiliza o modelo de usuário configurado no Django

    # Tenta obter o colaborador pelo email
    if not User.objects.filter(email=email).exists():
        # Cria o superusuário
        user = User.objects.create_superuser(
            email=email,
            password=password,
            username=username,
        )
        user.save()
        return user

    return None  # Retorna None caso o superusuário já exista

# Criando colaborador
superuser = create_superuser_if_not_exists(
    username='admin',
    email='admin@admin.com',
    password='admin',
)

exit()