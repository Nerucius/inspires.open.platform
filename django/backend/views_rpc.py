import json

from django.views import View
from django.http.response import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)

from backend.models import Project, Evaluation
from backend.views_api_csv import _authenticate_request



def json_response(data, status=200):
    return HttpResponse(json.dumps(data), status=status, content_type="application/json")


class UpdateProjectEvaluation(View):

    MAX_EVAL_VERSION = 2

    def get(self, request, project, *args, **kwargs):
        project = Project.objects.get(pk=project)
        try:
            _authenticate_request(request, project)
        except Exception:
            return HttpResponseForbidden()

        return json_response(
            {
                "id": project.id,
                "name": project.name,
                "eval_version": project.eval_version,
            }
        )

    def post(self, request, project, *args, **kwargs):
        project = Project.objects.get(pk=project)
        try:
            _authenticate_request(request, project)
        except Exception:
            return HttpResponseForbidden()

        request_version = json.loads(request.body)['eval_version']

        # Check for max version
        if project.eval_version == UpdateProjectEvaluation.MAX_EVAL_VERSION:
            return json_response({"detail": "Project is already at the latest evaluation version."}, 400)

        if project.eval_version >= request_version:
            return json_response({"detail": "Project is already at this version or newer."}, 400)

        if request_version > UpdateProjectEvaluation.MAX_EVAL_VERSION:
            return json_response({"detail": "Requested version does not exist."}, 400)

        # All clear, we can go ahead and migrate the project
        project.eval_version = request_version
        project.save()

        evals_to_delete = Evaluation.objects.filter(participation__project=project).all()
        evals_to_delete.delete()

        return json_response({"status": "OK", "eval_version": request_version, "evaluations_deleted": len(evals_to_delete)})
