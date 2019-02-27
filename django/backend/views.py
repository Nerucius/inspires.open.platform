from django.contrib import auth
from django.middleware import csrf
from django.http.response import HttpResponseBadRequest, HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers

import json


def test(request):
    return HttpResponse("OK")


def csrf_token(request):
    token = csrf.get_token(request)
    return HttpResponse(
        json.dumps({"csrf_token": token}), content_type="application/json"
    )


def login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    authUser = auth.authenticate(username=username, password=password)
    if authUser is not None:
        auth.login(request, authUser)
        return HttpResponse("OK")
    else:
        return HttpResponse("Invalid Credentials", status=401)


def logout(request):
    auth.logout(request)
    return HttpResponse("Logged out")


class CurrentUserView(viewsets.ReadOnlyModelViewSet):
    """ Returns the currently logged in user """

    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        queryset = models.User.objects
        if self.request.user.is_authenticated:
            return queryset.filter(pk=self.request.user.pk)
        return queryset.filter(pk="-1")


class RequirePKMixin(object):
    """ Mixin to require a pk parameter"""

    def get_queryset(self):
        if "pk" not in self.kwargs:
            raise Exception("Must provide a Query PK")
        return super().get_queryset()


# ===========================
# SIMPLE List Views
# ===========================


class UsersVS(viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects
    serializer_class = serializers.SimpleUserSerializer


class GroupsVS(viewsets.ReadOnlyModelViewSet):
    queryset = models.Group.objects
    serializer_class = serializers.SimpleGroupSerializer


# ===========================
# RELATED OBJECTS ENDPOINTS
# ===========================
