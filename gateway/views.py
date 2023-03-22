from django.shortcuts import render
from .models import JWT
import jwt
from UserProfile.models import CustomUser
from django.conf import settings
from datetime import datetime, timedelta
import random
import string
import os
from rest_framework import status
from rest_framework.views import APIView
from .serializers import LoginSerializer, RefreshSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .authentication import Authentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.

def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_access_token(payload):
    return jwt.encode({'exp': datetime.now() + timedelta(minutes=5), **payload}, settings.SECRET_KEY, algorithm='HS256')


def get_refresh_token():
    return jwt.encode({
        'exp': datetime.now() + timedelta(days=128),
        'data': get_random(10)
    }, settings.SECRET_KEY, algorithm="HS256")


class LoginView(APIView):
    serializer_calss = LoginSerializer

    def post(self, request):
        serializer = self.serializer_calss(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['email'], password=serializer.validated_data['password'])

        if not user:
            return Response({
                'error': 'Invalid email or password'
            }, status=status.HTTP_400_BAD_REQUEST)

        JWT.objects.filter(user_id=user.id).delete()

        access = get_access_token({
            'user': user.id
        })
        refresh = get_refresh_token()

        JWT.objects.create(
            user_id=user.id,
            access_token=access,
            refresh_token=refresh
        )
        return Response({
            'access': access,
            'refresh': refresh
        })


class RefreshView(APIView):
    serializer_calss = RefreshSerializer

    def post(self, request):
        serializer = self.serializer_calss(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            active_jwt = JWT.objects.get(
                refresh_token=serializer.validated_data['refresh_token'])
        except JWT.DoesNotExist:
            return Response({'error': "Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)

        if not Authentication.verify_token(serializer.validated_data['refresh_token']):
            return Response({
                "error": "Token is invalid or expired"
            })

        access = get_access_token({"user_id": active_jwt.user.id})

        refresh = get_refresh_token()

        active_jwt.save()

        return Response({
            'access': access,
            'refresh': refresh,
        })
