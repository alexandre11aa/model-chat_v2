from django.urls import path
from .views import chat_view, LoginView, user_list, upload_file

urlpatterns = [
    path("", LoginView.as_view(template_name="auth/login_page.html"), name="login-user"),
    path("login/", LoginView.as_view(template_name="auth/login_page.html"), name="login-user"),
    path('users/', user_list, name='user_list'),
    path("chat/<str:code>/", chat_view, name="chat-page"),
    path('upload-file/', upload_file, name='upload_file')
]