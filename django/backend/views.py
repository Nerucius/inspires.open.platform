from django.contrib import auth
from django.middleware import csrf
from django.http.response import HttpResponseBadRequest, HttpResponse

# from django_auto_prefetching import AutoPrefetchViewSetMixin, prefetch as auto_prefetch

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotFound

from django.contrib.contenttypes.models import ContentType

import json
import uuid

from . import email
from . import models
from . import serializers
from . import filters

from backend.views_rpc import json_response_error
from backend.permissions import HasWriteAccess


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
    if not term or len(term) < 3:
        return HttpResponseBadRequest(
            '{"error": "Missing  or invalid  parameter: `term` (min: 3 characters)"}',
            content_type="application/json",
        )

    # Projects
    projects = models.Project.objects.filter(name__icontains=term)
    projects |= models.Project.objects.filter(summary__icontains=term)
    projects |= models.Project.objects.filter(
        collaboration__structure__name__icontains=term
    )
    ## Filter by validated
    projects = projects.filter(collaboration__is_approved=True).filter(
        collaboration__structure__validation__is_approved=True
    )

    # Structures
    structures = models.Structure.objects.filter(name__icontains=term)
    structures |= models.Structure.objects.filter(summary__icontains=term)
    ## Filter by validated
    structures = structures.filter(validation__is_approved=True)

    objects = []
    objects += structures
    objects += projects

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

        real_user = models.User.objects.get(pk=authUser.pk)
        real_user.update_last_login()

        return HttpResponse("OK")
    else:
        return HttpResponse("Invalid Credentials", status=401)


def logout(request):
    auth.logout(request)
    return HttpResponse("OK")


def register(request):
    userdata = request.POST

    username = userdata["username"]
    password = userdata["password"]
    password2 = userdata["password2"]
    first_name = userdata["first_name"]
    last_name = userdata["last_name"]
    email = userdata["email"]

    if password != password2:
        return json_response_error("Passwords do not match.")

    if models.User.objects.filter(username=username).exists():
        return json_response_error("forms.rules.usernameInUse")

    if models.User.objects.filter(email=email).exists():
        return json_response_error("pages.register.emailTaken")

    try:
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

    except Exception as e:
        return json_response_error(e)

    return HttpResponse("OK")


def reset_password(request):
    from django.db.models import Q
    import random, string

    username = request.POST["username"]
    users = models.User.objects.filter(Q(email=username) | Q(username=username))

    if len(users) == 1:
        user = users[0]

        # Generate password reset token
        user.reset_password_token = str(uuid.uuid4())
        user.save()

        email.email_reset_password(user)

        return HttpResponse("OK")
    else:
        return HttpResponseBadRequest('{"detail":"No user found with that username or email."}')


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
        # Remove the eval token used for "Invite" users. This user now becomes a real user
        user.eval_token = None
        user.save()

    except Exception as e:
        return HttpResponseBadRequest(e)

    return HttpResponse("OK Password changed")


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
                return HttpResponse("Email not found", status=403)

        # Intercept response by base class to update the last_login
        try:
            response = super(CustomObtainAuthToken, self).post(request, args, kwargs)
            real_user = models.User.objects.get(username=request.data["username"])
            real_user.update_last_login()
        except Exception as e:
            raise e

        return response


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
    """Custom ViewSet that can have a simple serializer for LIST and one
    for the rest of views. use `detail_serializer_class`."""

    def get_serializer_class(self):
        # Dedicated Partial update Serializer
        if self.action == 'partial_update':
            if hasattr(self, 'update_serializer_class'):
                return self.update_serializer_class
        # Dedicated Non-list serializer
        if self.action != "list":
            if hasattr(self, "detail_serializer_class"):
                return self.detail_serializer_class
        return super(ListDetail, self).get_serializer_class()


class Orderable(object):
    ordering_fields = "__all__"


# ===========================
# User Related Viewsets
# ===========================


class UsersVS(ListDetail, viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    filterset_fields = ["id", "username"]

    serializer_class = serializers.SimpleUserSerializer
    update_serializer_class = serializers.CurrentUserSerializer
    detail_serializer_class = serializers.UserSerializer


class GroupsVS(viewsets.ReadOnlyModelViewSet):
    queryset = models.Group.objects.all()
    serializer_class = serializers.SimpleGroupSerializer


class CurrentUserVS(viewsets.ReadOnlyModelViewSet):
    """ Returns the logged in user details. """

    serializer_class = serializers.CurrentUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.User.objects
        return queryset.filter(pk=self.request.user.pk)


class CurrentUserEvaluationsVS(viewsets.ReadOnlyModelViewSet):
    """ Returns the logged in user's Evaluations. """

    serializer_class = serializers.EvaluationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.evaluations


# ===========================
# Datamodel Viewsets
# ===========================


class ProjectsVS(ListDetail, Orderable, viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    filterset_class = filters.ProjectFilter

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

        # print("get_queryset self.action")
        # print(self.action)

        # if self.action == "retrieve":
        #     return auto_prefetch(queryset, self.get_serializer_class())
        return queryset


class StructuresVS(ListDetail, Orderable, viewsets.ModelViewSet):
    queryset = models.Structure.objects.all()
    filterset_class = filters.StructureFilter

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

    filterset_fields = ["project", "structure", "partners"]


class NetworksVS(ListDetail, viewsets.ModelViewSet):
    queryset = models.Network.objects.all()
    serializer_class = serializers.SimpleNetworkSerializer
    detail_serializer_class = serializers.NetworkSerializer


class ParticipationVS(viewsets.ModelViewSet):
    queryset = models.Participation.objects.all()
    serializer_class = serializers.ParticipationSerializer

    filterset_fields = ["project", "user"]


class KeywordsVS(ListDetail, viewsets.ModelViewSet):
    queryset = models.Keyword.objects.all()
    serializer_class = serializers.SimpleKeywordSerializer
    detail_serializer_class = serializers.KeywordSerializer


class KnowledgeAreasVS(viewsets.ReadOnlyModelViewSet):
    queryset = models.KnowledgeArea.objects.all()
    serializer_class = serializers.KnowledgeAreaSerializer


class ProjectPhasesVS(viewsets.ReadOnlyModelViewSet):
    queryset = models.ProjectPhase.objects.all()
    serializer_class = serializers.ProjectPhaseSerializer


class ProjectAtPhasesVS(RequirePKMixin, viewsets.ModelViewSet):
    queryset = models.ProjectAtPhase.objects.all()
    serializer_class = serializers.ProjectAtPhaseSerializer


# ===========================
# Content Viewsets
# ===========================


class ContentVS(ListDetail, viewsets.ModelViewSet):
    queryset = models.Content.objects.filter(published=True)
    serializer_class = serializers.SimpleContentSerializer
    detail_serializer_class = serializers.ContentSerializer

    lookup_field = "slug"
    filterset_fields = ["locale", "master", "master__type", "master__parent"]


class ContentTypesVS(viewsets.ReadOnlyModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = serializers.ContentTypeSerializer


class AttachmentsVS(RequirePKMixin, viewsets.ModelViewSet):
    queryset = models.Attachment.objects.filter(deleted=False)
    serializer_class = serializers.AttachmentSerializer


class FeedbackVS(viewsets.ModelViewSet):
    queryset = models.Feedback.objects.all()
    serializer_class = serializers.FeedbackSerializer

    filterset_fields = ["feedback_type", "object_id", "content_type"]

    permission_classes = []

    def list(self, request, *args, **kwargs):
        if not request.user.is_administrator:
            raise PermissionDenied("Only for administrators")

        return super(FeedbackVS, self).list(request, *args, **kwargs)


# ===========================
# EVALUATION ENDPOINTS
# ===========================


class EvaluationVS(RequirePKMixin, viewsets.ModelViewSet):
    queryset = models.Evaluation.objects.all()
    serializer_class = serializers.EvaluationSerializer


class ProjectEvaluationsVS(RequirePKMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectEvaluationsSerializer
    filterset_fields = ["participation__user"]

    permission_classes = [IsAuthenticated, HasWriteAccess]


class ProjectEvaluationStatsVS(RequirePKMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectStatsSerializer


class EvaluationQuestionsVS(RequirePKMixin, viewsets.ModelViewSet):
    queryset = models.Evaluation.objects.all()
    serializer_class = serializers.EvaluationQuestionsSerializer


class EvaluationResponsesVS(RequirePKMixin, viewsets.ModelViewSet):
    queryset = models.Evaluation.objects.all()
    serializer_class = serializers.EvaluationResponsesSerializer

    permission_classes = [IsAuthenticated]


class QuestionVS(ListDetail, viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.SimpleQuestionSerializer
    detail_serializer_class = serializers.QuestionSerializer

    filterset_fields = ["version", "role", "phase"]


class AnswerVS(viewsets.ModelViewSet):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer


class ResponseVS(viewsets.ModelViewSet):
    """ Response API. If using as a listing, must provide project pk to validate. """

    queryset = models.Response.objects.all()
    serializer_class = serializers.ResponseSerializer
    filterset_class = filters.ResponseFilter

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # For list action, require project filter (specified in custom filter)
        if self.action == "list" and "project" not in self.request.GET:
            raise PermissionDenied(
                "Can't list global Response set. Please filter by 'project'"
            )
            try:
                project = models.Project.objects.get(pk=self.request.GET["project"])
            except:
                raise NotFound("Project not found")
            if not project.can_write(self.request.user):
                raise PermissionDenied(
                    "User does not have admin access to this project."
                )

        return super().get_queryset()
