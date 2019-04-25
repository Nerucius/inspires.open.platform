from rest_framework import routers

from backend import views

# Django REST Framework Router
router = routers.DefaultRouter()

router.register("user", views.CurrentUserVS, base_name="users/current")

# CRUD Views
router.register("users", views.UsersVS)
router.register("groups", views.GroupsVS)
router.register("structures", views.StructuresVS)
router.register("projects", views.ProjectsVS)
router.register("keywords", views.KeywordsVS)
router.register("collaborations", views.CollaborationsVS)
router.register("participations", views.ParticipationVS)
router.register("knowledgeareas", views.KnowledgeAreasVS)
router.register("projectphases", views.ProjectPhasesVS)
router.register("projectatphases", views.ProjectAtPhasesVS)

router.register("responses", views.ResponsesVS)

router.register("eval/evaluations", views.EvaluationVS)
router.register(
    "eval/project", views.ProjectEvaluationsVS, basename="project-evaluations"
)
router.register(
    "eval/questions", views.EvaluationQuestionsVS, basename="evaluation-questions"
)
router.register(
    "eval/responses", views.EvaluationResponsesVS, basename="evaluation-responses"
)


# Nested Objects Views
