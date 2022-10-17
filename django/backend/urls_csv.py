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
    path(
        "eval/<int:project>/tangram.csv", views.CSVProjectTangram.as_view()
    ),  #  Public Evaluation
    path("eval/<int:project>/global.csv", views.CSVProjectOverallPosition.as_view()),
    path("eval/<int:project>/phases.csv", views.CSVProjectPhases.as_view()),
    path(
        "eval/<int:project>/bullet_principles.csv",
        views.CSVProjectBulletPrinciples.as_view(),
    ),
    path(
        "eval/<int:project>/bullet_dimensions.csv",
        views.CSVProjectBulletDimensions.as_view(),
    ),
    path("eval/<int:project>/bullet_roles.csv", views.CSVProjectBulletRoles.as_view()),
    path("eval/<int:project>/heatmap.csv", views.CSVProjectHeatmap.as_view()),
    path(
        "export/<int:structure>/structure_summary.csv",
        views.CSVStructureSummaryExport.as_view(),
    ),
    path(
        "export/<int:project>/project_summary.csv",
        views.CSVProjectSummaryExport.as_view(),
    ),
    path(
        "export/<int:project>/project_evaluation.csv",
        views.export_project_evaluation,
    ),
    # TODO: Just a test
    path("export/test.csv", views.download_headers_test),
    path("export/all_own_projects.csv", views.CSVAllOwnProjectsExport.as_view()),
    path("export/all_own_structures.csv", views.CSVAllOwnStructresExport.as_view()),
    path("export/admin/projects/csv", views.CSVAdminAllProjects.as_view()),
    path("export/admin/projects/xlsx", views.XLSAdminAllProjects.as_view()),
    path("export/admin/structures/csv", views.CSVAdminAllStructures.as_view()),
    path("export/admin/structures/xlsx", views.XLSAdminAllStructures.as_view()),
    path("export/admin/evaluations/xlsx", views.XLSAdminEvaluationReport.as_view()),
    path("export/admin/qualitative/xlsx", views.XLSTextAnswersReport.as_view()),
]
