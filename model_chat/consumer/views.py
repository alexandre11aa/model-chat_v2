from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import View

from .forms import UserForm
from .models import CustomUser

@method_decorator(login_required, name='dispatch')
class UserRegisterUpdateView(View):
    form_class = UserForm
    template_name = '../templates/crud/register_page.html'
    success_url = reverse_lazy('user_list')

    def get_object(self):

        # Tenta pegar o objeto pelo ID nos parâmetros. Se não encontrar, retorna None.
        id = self.kwargs.get('id')

        if id:
            return get_object_or_404(CustomUser, id=id)

        return None

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        # Se o user existir, preenche o formulário com os dados atuais
        if user:
            form = self.form_class(instance=user)
        # Caso contrário, o formulário é vazio para um novo registro
        else:
            form = self.form_class()

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        # Se o user existir, será um update
        if user:
            form = self.form_class(
                request.POST, request.FILES, instance=user)
        # Caso contrário, cria um novo user
        else:
            form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            print(form.errors)

        # Caso o formulário não seja válido, renderiza novamente a página com erros
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name='dispatch')
class UserDeleteView(View):
    model = CustomUser
    template_name = '../templates/crud/list_page.html'

    def post(self, request, id, *args, **kwargs):
        
        # Obtém o objeto user ou retorna 404 se não existir
        user = get_object_or_404(self.model, id=id)

        # Deleta o user (uso de soft_delete ou delete direto)
        user.soft_delete()  # Ou user.delete() se for uma exclusão direta

        # Redireciona para a lista de user após a exclusão
        return redirect('user_list')