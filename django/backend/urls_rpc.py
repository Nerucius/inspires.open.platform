from django.urls import path

from backend import views_rpc as views

urlpatterns = [
    path("project/<int:project>/invite", views.InviteProjectParticipant.as_view()),
    path("projects/eval/update", views.UpdateAllProjectsEvaluation.as_view()),
]
