from django.shortcuts import render, redirect, get_object_or_404
from consumer.models import CustomUser
from .models import GroupChat

def create_group_chat(request):

    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return redirect("login-user")
    
    if request.method == 'POST':
        group_name = request.POST['group_name']
        group_chat = GroupChat.objects.create(name=group_name)

        # Obtém a lista de códigos de usuários do POST
        user_codes = request.POST.getlist('users')

        # Adiciona os usuários ao grupo usando o código UUID
        for code in user_codes:
            try:
                user = CustomUser.objects.get(code=code)  # Use o campo 'code'
                group_chat.users.add(user)  # Adiciona o usuário encontrado

            except CustomUser.DoesNotExist:
                print(f"Usuário com código {code} não encontrado.")

        return redirect('group_chat', group_chat_id=group_chat.id)

    users = CustomUser.objects.exclude(id=request.user.id)  # Obtém todos os usuários
    
    return render(request, 'auth/create_group_chat.html', {'users': users})

def groups_list(request):
    
    if not request.user.is_authenticated:
        return redirect("login-user")
    
    if request.user.is_superuser:
        # Se o usuário for superusuário, mostrar todos os grupos
        group_chats = GroupChat.objects.all()
    else:
        # Obtém todos os grupos de chat em que o usuário está participando
        group_chats = GroupChat.objects.filter(users=request.user)

    context = {
        'group_chats': group_chats,  # Lista de grupos de chat do usuário
        'logged_user': request.user,  # Usuário logado
    }

    return render(request, 'list_chats/groups_page.html', context)

def group_chat_view(request, group_chat_id):

    if not request.user.is_authenticated:
        return redirect("login-user")
    
    group_chat = get_object_or_404(GroupChat, id=group_chat_id)
    messages = group_chat.messages.all().order_by('timestamp')

    context = {
        'group_chat': group_chat,
        'messages': messages,
        'logged_user': request.user,
    }

    return render(request, 'chats/group_chat_page.html', context)
