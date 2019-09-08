from django.shortcuts import render, HttpResponse
from django.views import View
from django.conf import settings

from rest_framework.authtoken.models import Token

import requests
import json


def _get_request_user(request, project=None):
    try:
        header_auth = request.META["HTTP_AUTHORIZATION"]
    except:
        raise Exception("No user authentication provided")

    token = header_auth.split(" ")[-1]
    user = Token.objects.get(pk=token).user
    request.user = user
    return user


def _r(data, status=200):
    return HttpResponse(
        json.dumps(data), status=status, content_type="application/json"
    )


# Create your views here.
class UploadFileView(View):
    def post(self, request, filename, *args, **kwargs):

        user = _get_request_user(request)

        if not user.is_authenticated:
            return _r({"error": "User not authenticated"}, status=403)

        # Proxy request to Upload Server service
        response = requests.put(
            "%s/files/%s?token=secret" % (settings.UPLOAD_SERVER, filename),
            data=request.body,
            headers=request.headers,
        )

        # Read response from UPLOAD server
        response_data = json.loads(response.content)
        if "ok" in response_data and response_data["ok"] == True:
            file_url = "%s/%s" % (settings.UPLOAD_URL, filename)
            print(file_url)
            return _r({"url": file_url})

        # Return error response
        return HttpResponse(response, content_type="application/json")
