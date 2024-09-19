from django.shortcuts import render, redirect, get_object_or_404
from consumer.models import CustomUser
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse

def chatPage(request, code, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    
    # Tente buscar o usuário destino usando o campo 'code'
    try:
        target_user = CustomUser.objects.get(code=code)
    except CustomUser.DoesNotExist:
        return redirect("user_list")  # Redirecionar para a lista de usuários
    
    context = {
        "target_user": target_user
    }

    return render(request, "chatPage.html", context)

class LoginView(AuthLoginView):
    def get_success_url(self):
        # Redireciona para a lista de usuários após o login
        return reverse('user_list')

def user_list(request):
    users = CustomUser.objects.all()  # Obtém todos os usuários
    return render(request, 'userList.html', {'users': users})

def chat_view(request, target_code):
    target_user = get_object_or_404(CustomUser, code=target_code)
    return render(request, 'chatPage.html', {'target_user': target_user})
