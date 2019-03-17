from django.contrib import auth
from django.middleware import csrf
from django.http.response import HttpResponseBadRequest, HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

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
    return HttpResponse("OK")


def register(request):
    print(request.POST)
    try:
        invitation = request.POST["invitation"]

        assert invitation == "join-inspires-2019", "000 Invitation code does not match"

        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        assert password == password2, "001 Passwords don't match"
        assert not models.User.objects.filter(
            username=username
        ).exists(), "002 Username already exists"

        newUser = models.User.objects.create_user(
            username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        userGroup = models.Group.objects.get(name="Users")
        newUser.groups.add(userGroup)
        newUser.save()
        auth.login(request, newUser)

    except:
        import sys

        return HttpResponseBadRequest(sys.exc_info())

    return HttpResponse("OK")


class CurrentUserVS(viewsets.ReadOnlyModelViewSet):
    """ Returns the currently logged in user """

    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = models.User.objects
        if self.request.user.is_authenticated:
            return queryset.filter(pk=self.request.user.pk)
        return queryset.filter(pk="-1")


# ===========================
# Utility Mixins
# ===========================


class RequirePKMixin(object):
    """ Mixin to require a pk parameter"""

    def get_queryset(self):
        if "pk" not in self.kwargs:
            raise Exception("Must provide a Query PK")
        return super().get_queryset()


class ListDetail(object):
    """ Custom ViewSet that can have a simple serializer for LIST and one
        for the rest of views. use `detail_serializer_class`. """

    def get_serializer_class(self):
        if self.action != "list":
            if hasattr(self, "detail_serializer_class"):
                return self.detail_serializer_class
        return super(ListDetail, self).get_serializer_class()


class Orderable(object):
    ordering_fields = "__all__"


# ===========================
# Default Objects Serializers
# ===========================


class UsersVS(ListDetail, viewsets.ReadOnlyModelViewSet):
    queryset = models.User.objects
    filterset_fields = ["id", "username"]

    serializer_class = serializers.SimpleUserSerializer
    detail_serializer_class = serializers.UserSerializer


class GroupsVS(viewsets.ReadOnlyModelViewSet):
    queryset = models.Group.objects
    serializer_class = serializers.SimpleGroupSerializer


# ===========================
# Custom Serializers
# ===========================


class ProjectsVS(ListDetail, Orderable, viewsets.ModelViewSet):
    queryset = models.Project.objects
    filterset_fields = ["name", "collaboration__structure", "keywords", "managers"]

    serializer_class = serializers.SimpleProjectSerializer
    detail_serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        """ Filter out non-approved projects from main listing. """
        queryset = super(ProjectsVS, self).get_queryset()
        if self.action == "list":
            queryset = queryset.filter(collaboration__is_approved=True)
        return queryset


class StructuresVS(ListDetail, viewsets.ModelViewSet):
    queryset = models.Structure.objects
    filterset_fields = ["name", "collaboration__project", "managers"]

    serializer_class = serializers.SimpleStructureSerializer
    detail_serializer_class = serializers.StructureSerializer


class CollaborationsVS(viewsets.ModelViewSet):
    queryset = models.Collaboration.objects.all()
    serializer_class = serializers.CollaborationSerializer


class ParticipationVS(viewsets.ModelViewSet):
    queryset = models.Participation.objects.all()
    serializer_class = serializers.ParticipationSerializer


class KeywordsVS(ListDetail, viewsets.ModelViewSet):
    queryset = models.Keyword.objects
    serializer_class = serializers.SimpleKeywordSerializer
    detail_serializer_class = serializers.KeywordSerializer


# ===========================
# RELATED OBJECTS ENDPOINTS
# ===========================
