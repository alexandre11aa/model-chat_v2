from django.urls import path
from .views import chat_view, LoginView, user_list

urlpatterns = [
    path("chat/<str:code>/", chat_view, name="chat-page"),
    path("login/", LoginView.as_view(template_name="loginPage.html"), name="login-user"),
    path('users/', user_list, name='user_list'),
]