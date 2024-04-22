from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationCreate.as_view(), name='user_registration_create'), 
    path('login/', UserLogin.as_view(), name='user_login'), 
    path('users/', UserRegistrationList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserRegistrationList.as_view(), name='user-detail'),
    path('users/<int:pk>/update/', UserRegistrationUpdate.as_view(), name='user-update'), 
    path('users/delete/', UserRegistrationDelete.as_view(), name='user-delete'),
    path('users/delete/<int:pk>/', UserRegistrationDelete.as_view(), name='user-delete-by-id'),
]
