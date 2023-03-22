from django.urls import path, include
from .views import LoginView, RefreshView

urlpatterns = [
    path("login/", LoginView.as_view(),),
    path("refresh/", RefreshView.as_view(),),
]
