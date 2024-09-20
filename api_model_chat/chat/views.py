from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse
from django.db.models import Q
from consumer.models import CustomUser
from .models import Message

# Redireciona para a lista de usuários após o login
class LoginView(AuthLoginView):
    def get_success_url(self):
        return reverse('user_list')

def user_list(request):
    users = CustomUser.objects.all()  # Obtém todos os usuários
    return render(request, 'userList.html', {'users': users})

def chat_view(request, target_code):
    target_user = get_object_or_404(CustomUser, code=target_code)
    return render(request, 'chatPage.html', {'target_user': target_user})

def chat_view(request, code):
    if not request.user.is_authenticated:
        return redirect("login-user")
    
    target_user = get_object_or_404(CustomUser, code=code)

    # Recupera as mensagens trocadas entre o usuário logado e o usuário alvo
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=target_user) |
        Q(sender=target_user, receiver=request.user)
    ).order_by('timestamp')

    context = {
        'target_user': target_user,
        'messages': messages,
    }

    return render(request, 'chatPage.html', context)