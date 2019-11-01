from django.contrib import auth
from django.middleware import csrf
from django.http.response import HttpResponseBadRequest, HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotFound

from django.contrib.postgres.search import SearchVector

import json
import datetime

from . import email
from . import models
from . import serializers
from . import filters


def email_preview(request):
    from django import shortcuts
    from django.apps import apps

    email_name = request.GET["email_name"]
    context = request.GET.get("q", None)

    if context:
        context = json.loads(context)
        for key, value in context.items():
            if isinstance(value, int):
                model = apps.get_model("backend", model_name=key)
                context[key] = model.objects.get(pk=value)
    else:
        context = {}

    return shortcuts.render_to_response(email_name, context)


def csrf_token(request):
    token = csrf.get_token(request)
    return HttpResponse(
        json.dumps({"csrf_token": token}), content_type="application/json"
    )


def search(request):
    term = request.GET.get("term", None)
    if not term or len(term) < 4:
        return HttpResponseBadRequest(
            "missing required parameter: term (min: 4 characters)"
        )

    projects = models.Project.objects.filter(name__contains=term)
    projects |= models.Project.objects.filter(summary__contains=term)
    projects |= models.Project.objects.filter(
        collaboration__structure__name__contains=term
    )
    structures = models.Structure.objects.filter(name__contains=term)
    structures |= models.Structure.objects.filter(summary__contains=term)

    objects = []
    objects += projects
    objects += structures

    data = []

    for obj in objects:
        if isinstance(obj, models.Project):
            obj_data = serializers.SimpleProjectSerializer(obj).data
            obj_data["_type"] = "Project"
        if isinstance(obj, models.Structure):
            obj_data = serializers.SimpleStructureSerializer(obj).data
            obj_data["_type"] = "Structure"
        data += [obj_data]

    response = JSONRenderer().render({"count": len(data), "data": data})
    return HttpResponse(response)


def log_error(request):
    from django.contrib.admin.models import LogEntry
    from django.contrib.admin.models import ADDITION
    from backend.models import User

    message = request.GET.get("message", "no message")
    error = request.GET.get("error", "no error")
    user = request.GET.get("user", 1)

    try:
        user = User.objects.get(pk=user)
    except Exception:
        user = User.objects.get(pk=1)

    log = LogEntry(
        user=user,
        object_repr="ERROR",
        action_flag=ADDITION,
        change_message=message + " | Dump: " + error,
    )
    log.save()

    return HttpResponse('{"message": "error logged" }', content_type="application/json")


def login(request):

    username = request.POST["username"]
    password = request.POST["password"]

    # If using email as login, retrieve username
    if "@" in username:
        try:
            username = models.User.objects.get(email=username).username
        except:
            return HttpResponse("Email not found", status=401)

    authUser = auth.authenticate(username=username, password=password)
    if authUser is not None:
        auth.login(request, authUser)
        return HttpResponse("OK")
    else:
        return HttpResponse("Invalid Credentials", status=401)


class CustomObtainAuthToken(ObtainAuthToken):
    """ Custom Token auth to also login with email """

    def post(self, request, *args, **kwargs):
        username = request.data["username"]
        if "@" in username:
            try:
                # Find user and get his
                user = models.User.objects.get(email=username)
                request.data["username"] = user.username
            except:
                return HttpResponse("Email not found", status=401)

        return super(CustomObtainAuthToken, self).post(request, args, kwargs)


def logout(request):
    auth.logout(request)
    return HttpResponse("OK")


def register(request):
    userdata = request.POST
    try:
        # invitation = userdata["invitation"]
        # assert invitation == "join-inspires-2019", "000 Invitation code does not match"

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


def reset_password(request):
    from django.db.models import Q
    import random, string

    username = request.POST["username"]
    users = models.User.objects.filter(Q(email=username) | Q(username=username))

    if len(users) == 1:
        user = users[0]

        # Generate password reset token
        letters = string.ascii_letters + string.digits
        token = "".join(random.choice(letters) for i in range(128))
        user.reset_password_token = token
        user.save()

        email.email_reset_password(user)

        return HttpResponse("OK")
    else:
        return HttpResponseBadRequest("No user found")


def reset_password_submit(request):
    formdata = request.POST
    token = request.POST.get("token", "")
    password = request.POST.get("password", "")
    password2 = request.POST.get("password2", "")

    assert token != "", "001 token not provided"

    try:
        user = models.User.objects.get(reset_password_token=token)
        # user.reset_password_token = ""

        assert password == password2, "003 password missmatch"
        user.reset_password_token = ""
        user.set_password(password)
        user.save()

    except Exception:
        return HttpResponseBadRequest("002 user for token not found")

    return HttpResponse("OK Password changed")


class CurrentUserVS(viewsets.ModelViewSet):
    """ Returns the currently logged in user """

    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.User.objects
        return queryset.filter(pk=self.request.user.pk)


# ===========================
# Utility Mixins
# ===========================


class RequirePKMixin(object):
    """ Mixin to require a pk parameter"""

    def get_queryset(self):
        if self.action == "list" and "pk" not in self.kwargs:
            raise PermissionDenied(
                "This list endpoint requries a primary key to access."
            )
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


class UsersVS(ListDetail, viewsets.ModelViewSet):
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
    filterset_fields = [
        "name",
        "collaboration__structure",
        "keywords",
        "participants",
        "knowledge_area",
        "country_code",
    ]

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
        nonvalid = self.request.GET.get("nonvalidated", False)
        if nonvalid and self.request.user.is_administrator:
            return super(StructuresVS, self).get_queryset().filter(validation=None)

        queryset = super(StructuresVS, self).get_queryset()
        if self.action == "list":
            queryset = queryset.filter(validation__is_approved=True)
        return queryset


class StructureValidationsVS(viewsets.ModelViewSet):
    queryset = models.StructureValidation.objects.all()
    serializer_class = serializers.StructureValidationSerializer

    filterset_fields = ["structure"]


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
    """ Response API. If using as a listing, must provide project pk to validate. """

    queryset = models.Response.objects.all()
    serializer_class = serializers.ResponseSerializer
    filterset_class = filters.ResponseFilter

    def get_queryset(self):
        if self.action == "list" and "project" not in self.request.GET:
            raise PermissionDenied(
                "Can't list global Response set. Please filter by 'project'"
            )
        try:
            project = models.Project.objects.get(pk=self.request.GET["project"])
        except:
            raise NotFound("Project not found")
        if not project.can_write(self.request.user):
            raise PermissionDenied("User does not have admin access to this project.")

        return super().get_queryset()


# ===========================
# RELATED OBJECTS ENDPOINTS
# ===========================
