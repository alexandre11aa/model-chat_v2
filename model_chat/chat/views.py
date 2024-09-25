from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse
from django.db.models import Q
from consumer.models import CustomUser
from .models import DuoMessage

# Redireciona para a lista de usuários após o login
class LoginView(AuthLoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user_list')  # Redireciona para a lista de usuários
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('user_list')

def user_list(request):
    users = CustomUser.objects.exclude(id=request.user.id)  # Obtém todos os usuários
    logged_user = request.user  # Usuário logado
    return render(request, 'list_chats/duo_users_page.html', {'users': users, 'logged_user': logged_user})

def chat_view(request, code):
    if not request.user.is_authenticated:
        return redirect("login-user")

    target_user = get_object_or_404(CustomUser, code=code)

    messages = DuoMessage.objects.filter(
        Q(sender=request.user, receiver=target_user) |
        Q(sender=target_user, receiver=request.user)
    ).order_by('timestamp')

    context = {
        'target_user': target_user,
        'messages': messages,
        'logged_user': request.user,
    }

    return render(request, 'chats/duo_chat_page.html', context)