from django.urls import path

from backend import views_api_csv as views

urlpatterns = [
    # path("csrf_token/", views.csrf_token),
    path("eval/<int:project>/global.csv", views.csv_overall_position),
    path("eval/<int:project>/phases.csv", views.csv_phases),
    path("eval/<int:project>/bullets.csv", views.csv_bullets),
    path("eval/<int:project>/heatmap.csv", views.csv_heatmap),
]
