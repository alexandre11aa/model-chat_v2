import os

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse
from django.db.models import Q
from consumer.models import CustomUser
from .models import DuoMessage, DuoFile
from django.http import JsonResponse

# Redireciona para a lista de usuários após o login
class LoginView(AuthLoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user_list')  # Redireciona para a lista de usuários
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('user_list')

def user_list(request):
   #users = CustomUser.objects.filter(deleted_at__isnull=True, is_active=True).exclude(id=request.user.id)
    users = CustomUser.objects.filter(is_active=True).exclude(id=request.user.id)
    logged_user = request.user  # Usuário logado

    # Contar as mensagens não lidas e os arquivos não lidos de cada usuário
    unread_messages = {
        user.id: (DuoMessage.objects.filter(sender=user, receiver=logged_user, is_read=False).count() +
                  DuoFile.objects.filter(sender=user, receiver=logged_user, is_read=False).count())  # Contar mensagens e arquivos não lidos
        for user in users
    }

    return render(request, 'list_chats/duo_users_page.html', {
        'users': users,
        'logged_user': logged_user,
        'unread_messages': unread_messages  # Passando a contagem combinada para o template
    })

def chat_view(request, code):
    if not request.user.is_authenticated:
        return redirect("login-user")

    target_user = get_object_or_404(CustomUser, code=code)

    # Obter mensagens e arquivos trocados
    messages = DuoMessage.objects.filter(
        Q(sender=request.user, receiver=target_user) |
        Q(sender=target_user, receiver=request.user)
    ).order_by('timestamp')

    files = DuoFile.objects.filter(
        Q(sender=request.user, receiver=target_user) |
        Q(sender=target_user, receiver=request.user)
    ).order_by('timestamp')

    # Marcar as mensagens recebidas como lidas
    DuoMessage.objects.filter(receiver=request.user, sender=target_user, is_read=False).update(is_read=True)

    # Marcar os arquivos recebidos como lidos
    DuoFile.objects.filter(receiver=request.user, sender=target_user, is_read=False).update(is_read=True)

    # Combinar mensagens e arquivos em uma lista
    combined = []
    for message in messages:
        combined.append({'type': 'message', 'content': message})
    for file in files:
        combined.append({'type': 'file', 'content': file})

    # Ordenar a lista combinada pelo timestamp
    combined.sort(key=lambda x: x['content'].timestamp)

    context = {
        'target_user': target_user,
        'combined': combined,  # Passando a lista combinada para o contexto
        'logged_user': request.user,
    }

    return render(request, 'chats/duo_chat_page.html', context)

def upload_file(request):

    # Obtém o diretório atual
    current_directory = os.getcwd()

    # Define o caminho para o diretório 'uploads'
    uploads_directory = os.path.join(current_directory, 'uploads')

    # Verifica se o diretório 'uploads' existe e o cria se não existir
    if not os.path.exists(uploads_directory):
        os.makedirs(uploads_directory)

    if request.method == 'POST':
        file = request.FILES.get('file')
        filename = request.POST.get('filename')  # Para obter o nome do arquivo

        if file:
            # Salva o arquivo no diretório desejado
            save_path = os.path.join(uploads_directory, filename)  # Define o caminho completo
            with open(save_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            return JsonResponse({'success': True, 'filename': filename})
        
    return JsonResponse({'error': 'Invalid request'}, status=400)