from django.urls import path
from .views import ForgotPasswordView, ResetPasswordView, UserProfileUpdateView, UserRegistrationView, UserProfileView, UserPasswordView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    # path('login/', UserLoginView.as_view(), name='user_login'),

    # path('logout/', UserLogoutView.as_view(), name='user-logout'),

    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(),
         name='edit_user_profile'),
    path('profile/password/', UserPasswordView.as_view(), name='user_password'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset_password'),
    # path('reset_password/uidb64=<uidb64>/token=<token>/', ResetPasswordView.as_view(), name='reset_password')
    # path('reset_password/', ResetPasswordView.as_view(), name='reset_password')
    

]
