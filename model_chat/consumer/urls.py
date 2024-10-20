from django.urls import path
from .views import *

urlpatterns = [
    path('register_user/', UserRegisterUpdateView.as_view(), name='register_user'),
    path('update_user/<int:id>/', UserRegisterUpdateView.as_view(), name='update_user'),
    path('delete_user/<int:id>/', UserDeleteView.as_view(), name='delete_user'),
]