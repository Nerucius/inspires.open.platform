from rest_framework import routers

from backend import views

# Django REST Framework Router
router = routers.DefaultRouter()

router.register("user", views.CurrentUserView, base_name="users/current")

# CRUD Views
router.register("users", views.UsersVS)
router.register("groups", views.GroupsVS)

# Nested Objects Views

