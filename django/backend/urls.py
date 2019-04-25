"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token

from backend import views
from backend import routers

urlpatterns = [
    # path("csrf_token/", views.csrf_token),
    path("user/login/", views.login),
    path("user/logout/", views.logout),
    path("user/register/", views.register),
    path("v1/log-error", views.log_error),
    path("v1/emailpreview", views.email_preview, name="email_preview"),
    path("v1/", include(routers.router.urls)),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]

if settings.DEBUG:
    urlpatterns += [
        path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
    ]
