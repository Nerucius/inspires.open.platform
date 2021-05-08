from rest_framework import routers

from backend import views

# Django REST Framework Router
router = routers.DefaultRouter()

router.register(
    "user/evaluations", views.CurrentUserEvaluationsVS, basename="user/evaluations"
)
router.register("user", views.CurrentUserVS, basename="user/current")

# CRUD Views
router.register("users", views.UsersVS)
router.register("groups", views.GroupsVS)
router.register("structures/validations", views.StructureValidationsVS)
router.register("structures", views.StructuresVS)
router.register("networks", views.NetworksVS)
router.register("projects", views.ProjectsVS)
router.register("keywords", views.KeywordsVS)
router.register("collaborations", views.CollaborationsVS)
router.register("participations", views.ParticipationVS)
router.register("knowledgeareas", views.KnowledgeAreasVS)
router.register("projectphases", views.ProjectPhasesVS)
router.register("projectatphases", views.ProjectAtPhasesVS)

router.register("contenttypes", views.ContentTypesVS)
router.register("attachments", views.AttachmentsVS)

# Content

router.register("contents", views.ContentVS)

# Evaluation Routes

router.register("question", views.QuestionVS)
router.register("response", views.ResponseVS)
router.register("answer", views.AnswerVS)
router.register("eval/evaluations", views.EvaluationVS)
router.register(
    "eval/project", views.ProjectEvaluationsVS, basename="project-evaluations"
)
router.register(
    "eval/project/stats", views.ProjectEvaluationStatsVS, basename="project-evaluations"
)
router.register(
    "eval/questions", views.EvaluationQuestionsVS, basename="evaluation-questions"
)
router.register(
    "eval/responses", views.EvaluationResponsesVS, basename="evaluation-responses"
)

# Nested Objects Views
