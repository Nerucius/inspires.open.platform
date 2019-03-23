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

# Nested Objects Views
