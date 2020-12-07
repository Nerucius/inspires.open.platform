import json
import uuid

from decouple import config

from django.views import View
from django.http.response import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)

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
                assert project.can_write(request.user), "Not authorized to modify this Project."
                assert project.structure != None, "Project not linked to any structure."
                assert project.structure.validation != None, "Structure not validated."
                assert project.structure.validation.is_approved, "Structure not validated."
                assert project.collaboration.is_approved, "Your Structure has not validated this Project."
        except Exception as e:
            return json_response_error(e)

        request_data = json.loads(request.body)

        # Create a fictitious email if none is sent
        if 'email' in request_data and request_data['email'] != '':
            user_username = request_data['email']
            user_email = request_data['email']
        else:
            user_username = str(uuid.uuid4())
            user_email = user_username + '@app.inspiresproject.com'

        # Check for existing users
        if User.objects.filter(email=user_email).exists():
            return json_response_error("pages.register.emailTaken")

        # Create user including empty field defaults
        newUser = User(
            username=user_username,
            first_name=request_data['first_name'],
            last_name=request_data['last_name'],
            email=user_email,
            hide_realname='hide_realname' in request_data and request_data['hide_realname'],
            gender=request_data['gender'] if 'gender' in request else '',
            institution=request_data['institution'] if 'institution' in request else '',
        )
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
            role=ParticipationRole.objects.get(pk=request_data['role'])
        )

        try:
            participation.save()
        except Exception as e:
            newUser.delete()
            return json_response_error("Could not link User to Project: " + str(e))


        return json_response(
            {
                "status": "OK",
                "user_id": newUser.pk,
                "eval_token": newUser.eval_token
            }
        )
