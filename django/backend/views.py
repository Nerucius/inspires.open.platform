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


def log_error(request):
    from django.contrib.admin.models import LogEntry
    from django.contrib.admin.models import ADDITION
    from backend.models import User

    message = request.GET.get("message", "no message")
    user = request.GET.get("user", 1)
    log = LogEntry(
        user=User.objects.get(pk=user),
        object_repr="ERROR",
        action_flag=ADDITION,
        change_message=message,
    )
    log.save()

    return HttpResponse("OK")


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
    userdata = request.POST
    print(userdata)
    try:
        invitation = userdata["invitation"]

        assert invitation == "join-inspires-2019", "000 Invitation code does not match"

        username = userdata["username"]
        password = userdata["password"]
        password2 = userdata["password2"]
        first_name = userdata["first_name"]
        last_name = userdata["last_name"]
        email = userdata["email"]

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
        # auth.login(request, newUser)

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
        if self.action == "list" and "pk" not in self.kwargs:
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
    queryset = models.User.objects.all()
    filterset_fields = ["id", "username"]

    serializer_class = serializers.SimpleUserSerializer
    detail_serializer_class = serializers.UserSerializer


class GroupsVS(viewsets.ReadOnlyModelViewSet):
    queryset = models.Group.objects.all()
    serializer_class = serializers.SimpleGroupSerializer


# ===========================
# Custom Serializers
# ===========================


class ProjectsVS(ListDetail, Orderable, viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    filterset_fields = ["name", "collaboration__structure", "keywords", "participants", "knowledge_area"]

    serializer_class = serializers.SimpleProjectSerializer
    detail_serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        """ Filter out non-approved projects from main listing. """
        queryset = super(ProjectsVS, self).get_queryset()
        if self.action == "list":
            queryset = queryset.filter(collaboration__is_approved=True)
            queryset = queryset.filter(
                collaboration__structure__validation__is_approved=True
            )
        return queryset


class StructuresVS(ListDetail, Orderable, viewsets.ModelViewSet):
    queryset = models.Structure.objects.all()
    filterset_fields = ["name", "collaboration__project", "managers"]

    serializer_class = serializers.SimpleStructureSerializer
    detail_serializer_class = serializers.StructureSerializer

    def get_queryset(self):
        """ Filter out non-approved projects from main listing. """
        queryset = super(StructuresVS, self).get_queryset()
        if self.action == "list":
            queryset = queryset.filter(validation__is_approved=True)
        return queryset


class CollaborationsVS(viewsets.ModelViewSet):
    queryset = models.Collaboration.objects.all()
    serializer_class = serializers.CollaborationSerializer

    filterset_fields = ["project", "structure"]


class ParticipationVS(viewsets.ModelViewSet):
    queryset = models.Participation.objects.all()
    serializer_class = serializers.ParticipationSerializer

    filterset_fields = ["project", "user"]


class KeywordsVS(ListDetail, viewsets.ModelViewSet):
    queryset = models.Keyword.objects.all()
    serializer_class = serializers.SimpleKeywordSerializer
    detail_serializer_class = serializers.KeywordSerializer


class KnowledgeAreasVS(viewsets.ModelViewSet):
    queryset = models.KnowledgeArea.objects.all()
    serializer_class = serializers.KnowledgeAreaSerializer


class ProjectPhasesVS(viewsets.ModelViewSet):
    queryset = models.ProjectPhase.objects.all()
    serializer_class = serializers.ProjectPhaseSerializer


class ProjectAtPhasesVS(RequirePKMixin, viewsets.ModelViewSet):
    queryset = models.ProjectAtPhase.objects.all()
    serializer_class = serializers.ProjectAtPhaseSerializer


# ===========================
# EVALUATION ENDPOINTS
# ===========================


class EvaluationVS(RequirePKMixin, viewsets.ModelViewSet):
    queryset = models.Evaluation.objects.all()
    serializer_class = serializers.EvaluationSerializer


class ProjectEvaluationsVS(RequirePKMixin, viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectEvaluationsSerializer


class EvaluationQuestionsVS(RequirePKMixin, viewsets.ModelViewSet):
    queryset = models.Evaluation.objects.all()
    serializer_class = serializers.EvaluationQuestionsSerializer


class EvaluationResponsesVS(RequirePKMixin, viewsets.ModelViewSet):
    queryset = models.Evaluation.objects.all()
    serializer_class = serializers.EvaluationResponsesSerializer


class QuestionVS(ListDetail, viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.SimpleQuestionSerializer
    detail_serializer_class = serializers.QuestionSerializer


class ResponseVS(viewsets.ModelViewSet):
    queryset = models.Response.objects.all()
    serializer_class = serializers.ResponseSerializer


# ===========================
# RELATED OBJECTS ENDPOINTS
# ===========================
