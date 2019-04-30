from django.urls import path

from backend import views_api_csv as views

urlpatterns = [
    path("eval/all_responses.csv", views.CSVAllResponsesDegree.as_view()),
    path("eval/all_responses_multi.csv", views.CSVAllResponsesMultiple.as_view()),
    path("eval/<int:project>/responses.csv", views.CSVProjectResponsesDegree.as_view()),
    path(
        "eval/<int:project>/responses_multi.csv",
        views.CSVProjectResponsesMultiple.as_view(),
    ),
    path("eval/<int:project>/global.csv", views.CSVProjectOverallPosition.as_view()),
    path("eval/<int:project>/phases.csv", views.CSVProjectPhases.as_view()),
    path("eval/<int:project>/bullets.csv", views.csv_bullets),
    path("eval/<int:project>/heatmap.csv", views.csv_heatmap),
]
