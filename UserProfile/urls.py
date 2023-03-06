from django.urls import path
from .views import UserLogoutView, UserProfileUpdateView, UserRegistrationView, UserLoginView, UserProfileView, UserPasswordView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', UserLoginView.as_view(), name='user_login'),

    path('logout/', UserLogoutView.as_view(), name='user-logout'),

    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(),
         name='edit_user_profile'),
    path('profile/password/', UserPasswordView.as_view(), name='user_password'),
    
]
