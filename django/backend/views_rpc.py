import json
import uuid

from decouple import config

from django.views import View
from django.http.response import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from django.db import transaction

from rest_framework.authtoken.models import Token

from backend.models import Project, Evaluation, Participation, ParticipationRole
from backend.views_api_csv import _authenticate_request
from backend.serializers import SimpleUserSerializer

from backend.models import User, Group


def json_response(data, status=200):
    return HttpResponse(
        json.dumps(data), status=status, content_type="application/json"
    )


def json_response_error(exception, status=400):
    data = {"detail": str(exception)}
    return HttpResponse(
        json.dumps(data), status=status, content_type="application/json"
    )


class InviteProjectParticipant(View):
    def post(self, request, project, *args, **kwargs):
        project = Project.objects.get(pk=project)
        try:
            _authenticate_request(request, project)
            if not request.user.is_superuser:
                assert project.can_write(
                    request.user
                ), "Not authorized to modify this Project."
                assert project.structure != None, "Project not linked to any structure."
                assert project.structure.validation != None, "Structure not validated."
                assert (
                    project.structure.validation.is_approved
                ), "Structure not validated."
                assert (
                    project.collaboration.is_approved
                ), "Your Structure has not validated this Project."
        except Exception as e:
            return json_response_error(e)

        request_data = json.loads(request.body)

        # Create a fictitious email if none is sent
        if "email" in request_data and request_data["email"] != "":
            user_username = request_data["email"]
            user_email = request_data["email"]
        else:
            user_username = str(uuid.uuid4())
            user_email = user_username + "@app.inspiresproject.com"

        # Check for existing users
        if User.objects.filter(email=user_email).exists():
            return json_response_error("pages.register.emailTaken")

        # Create user including empty field defaults
        newUser = User(
            username=user_username,
            email=user_email,
            first_name=request_data["first_name"],
            last_name=request_data["last_name"],
        )

        # Optional fields
        if "gender" in request_data:
            newUser.gender = request_data["gender"]
        if "education_level" in request_data:
            newUser.education_level = request_data["education_level"]
        if "institution" in request_data:
            newUser.institution = request_data["institution"]
        if "hide_realname" in request_data and request_data["hide_realname"]:
            newUser.hide_realname = True

        try:
            newUser.save()
            userGroup = Group.objects.get(name="Users")
            newUser.groups.add(userGroup)
            newUser.save()
        except Exception as e:
            return json_response_error("Failed to create User: " + str(e))

        # Get the user a valid login token:
        token, created = Token.objects.get_or_create(user=newUser)
        newUser.eval_token = token.key
        newUser.save()

        # User created, now we have to link them to this project
        participation = Participation(
            user=newUser,
            project=project,
            role=ParticipationRole.objects.get(pk=request_data["role"]),
        )

        try:
            participation.save()
        except Exception as e:
            newUser.delete()
            return json_response_error("Could not link User to Project: " + str(e))

        return json_response(
            {"status": "OK", "user_id": newUser.pk, "eval_token": newUser.eval_token}
        )


CURRENT_EVAL_VERSION = 1
LATEST_EVAL_VERSION = 2


class UpdateAllProjectsEvaluation(View):
    """ API to update all existing Projects without evaluation data to the latest version """

    def post(self, request, *args, **kwargs):
        _authenticate_request(request)
        if not request.user.is_superuser:
            return json_response_error("User must be super-user to trigger update")

        request_data = json.loads(request.body)

        projects = Project.objects.filter(eval_version__lt=LATEST_EVAL_VERSION)
        projects_to_update = []
        projects_to_not_update = []

        for project in projects:
            project_has_evals = Evaluation.objects.filter(
                phase__project=project
            ).exists()

            if not project_has_evals:
                projects_to_update += [project]
            else:
                projects_to_not_update += [project]

        if "execute" in request_data and request_data["execute"] == True:
            status = "OK"
            try:
                with transaction.atomic():
                    for project in projects_to_update:
                        project.eval_version = LATEST_EVAL_VERSION
                        project.save()
            except Exception as e:
                return json_response_error(e)

        else:
            status = "DRY_RUN"

        return json_response(
            {
                "status": status,
                "projects_to_update": len(projects_to_update),
                "projects_to_not_update": len(projects_to_not_update),
            }
        )
