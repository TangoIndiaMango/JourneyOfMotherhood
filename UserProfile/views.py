from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.db.models import Q, Count
from UserProfile.models import CustomUser
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .serializers import CustomUserSerializer, UserProfileSerializer, UserPasswordSerializer, UserProfileUpdateSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserRegistrationView(APIView):
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'gender': user.gender,
                    'date_of_birth': user.date_of_birth,
                    'about_me': user.about_me,
                    'created_at': user.created_at,
                }
        
            })
        else:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logout successful.'})


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        user = request.user
        print(f"user is {user}")
        posts_count = user.posts.count()
        followers_count = user.followers.count()
        following_count = user.following.count()
        user.posts_count = posts_count
        user.followers_count = followers_count
        user.following_count = following_count
        serializer = self.serializer_class(user)
        return Response(serializer.data)


class UserProfileUpdateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileUpdateSerializer

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(
                serializer.validated_data['new_password'])
            request.user.save()
            return Response({'detail': 'Password updated successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == user_to_follow:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user_to_follow)
        request.user.following_count += 1
        request.user.save()

        return Response({'detail': f'You are now following {user_to_follow.username}.'}, status=status.HTTP_201_CREATED)


class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = get_user_model().objects.filter(email=email).first()
        if user is not None:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_password_url = f"{settings.BASE_URL}/user/reset_password/{uidb64}/{token}/"
            subject = 'Reset Password'
            message = f'Click the link below to reset your password: {reset_password_url}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject, message, from_email,
                      recipient_list, fail_silently=False)
            return Response({'detail': 'A reset password link has been sent to your email.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid email.'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            return User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            return Response({'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid reset password link.'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = self.get_user(uidb64)
            if user is not None and PasswordResetTokenGenerator().check_token(user, token):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid reset password link.'}, status=status.HTTP_400_BAD_REQUEST)




class TopUsersView(APIView):
    def get(self, request, format=None):
        queryset = CustomUser.objects.annotate(
            num_followers=Count('followers')
        ).annotate(
            following_count=Count('following')
        ).annotate(
            post_count=Count('posts')
        ).order_by('-post_count')[:10]
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)



# class ResetPasswordView(APIView):
#     serializer_class = ResetPasswordSerializer

#     def get_user(self, uidb64):
#         try:
#             uid = urlsafe_base64_decode(uidb64).decode()
#             return User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             return None

#     def post(self, request, uidb64, token):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             user = self.get_user(request.params.query(uidb64))
#             if user is not None and PasswordResetTokenGenerator().check_token(user, request.params.query(token)):
#                 user.set_password(serializer.validated_data['new_password'])
#                 user.save()
#                 return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid reset password link.'}, status=status.HTTP_400_BAD_REQUEST)


# class ResetPasswordView(APIView):
#     serializer_class = ResetPasswordSerializer

#     def post(self, request, uidb64, token):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             try:
#                 uid = force_text(urlsafe_base64_decode(uidb64))
#                 user = User.objects.get(pk=uid)
#             except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#                 user = None
#             token_generator = PasswordResetTokenGenerator()
#             if user is not None and token_generator.check_token(user, token):
#                 user.set_password(serializer.validated_data['new_password'])
#                 user.save()
#                 return Response({'detail': 'Password updated successfully.'}, status=status.HTTP_200_OK)
#         return Response({'detail': 'Invalid reset password link.'}, status=status.HTTP_400_BAD_REQUEST)
