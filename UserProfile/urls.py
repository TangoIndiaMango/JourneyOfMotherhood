from django.urls import path, include
from .views import ChangePasswordView, ConfirmResetPasswordView, FollowView, ResetPasswordView, TopUsersView, FollowDeleteView, UserLoginView, UserLogoutView, UserProfileUpdateView, UserRegistrationView, UserProfileView, UserPasswordView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', UserLoginView.as_view(), name='user_login_token'),

    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(),
         name='edit_user_profile'),
    path('profile/password/', UserPasswordView.as_view(), name='user_password'),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    # path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    
    # path('reset_password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('password_reset/', include('django_rest_passwordreset.urls'), name='password_reset'),
    
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('topusers/', TopUsersView.as_view(), name='top_users'),
    path('follow/<int:user_id>/', FollowView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', FollowDeleteView.as_view(), name='unfollow'),
    path('confirm-reset-password/<str:uidb64>/<str:token>/', ConfirmResetPasswordView.as_view(), name='confirm-reset-password'),
    path('topusers/', TopUsersView.as_view(), name='top_users'),
    


    # path('reset_password/<uidb64>&<token>/', ResetPasswordView.as_view(), name='reset_password'),
    # path('reset_password/', ResetPasswordView.as_view(), name='reset_password')
    

]
