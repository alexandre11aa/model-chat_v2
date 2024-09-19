from django.urls import path
from .views import chatPage, LoginView, user_list

urlpatterns = [
    path("chat/<str:code>/", chatPage, name="chat-page"),
    path("login/", LoginView.as_view(template_name="loginPage.html"), name="login-user"),
    path('users/', user_list, name='user_list'),  # Certifique-se de que a view esteja corretamente configurada
]