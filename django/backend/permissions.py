from rest_framework import permissions

from backend.models import TrackableModel


class CustomPermissionSet(permissions.DjangoModelPermissions):
    """Custom application logic Permissions. Premise is user MUST
    be logged in for any kind of permission.
    Runs the DjangoModelPermissions schema first so that
    group permissions work.
    """

    CREATE_METHOD = "POST"
    authenticated_users_only = False

    # Custom permission map with VIEW permission added
    # perms_map = {
    #     "GET": ["%(app_label)s.view_%(model_name)s"],
    #     "OPTIONS": ["%(app_label)s.view_%(model_name)s"],
    #     "HEAD": ["%(app_label)s.view_%(model_name)s"],
    #     "POST": ["%(app_label)s.add_%(model_name)s"],
    #     "PUT": ["%(app_label)s.change_%(model_name)s"],
    #     "PATCH": ["%(app_label)s.change_%(model_name)s"],
    #     "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    # }

    def has_permission(self, request, view):
        """ Separate into read VS modify. """

        if request.user.is_superuser:
            return True

        # Next line skips views without a queryset (API root)
        if not hasattr(view, "get_queryset"):
            return True

        if request.method in permissions.SAFE_METHODS:
            return self.has_read_permission(request, view)
        return self.has_write_permission(request, view)

    def has_object_permission(self, request, view, obj):
        """ Separate into read VS modify. """

        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return self.has_object_read_permission(request, view, obj)
        return self.has_object_write_permission(request, view, obj)

    def has_read_permission(self, request, view):
        """ For read check only the `view_XXX` model permission. """

        has_model_perm = super(CustomPermissionSet, self).has_permission(request, view)
        return has_model_perm

    def has_write_permission(self, request, view):
        """Define write permission to a model as two different options:
        1. Is creating a new Object: check "can_create" class method.
        2. Is patching an existing object: check django permission.
        In all cases the model permission is checked.
        """

        has_model_perm = super(CustomPermissionSet, self).has_permission(request, view)

        if request.method == self.CREATE_METHOD:
            model_class = view.get_queryset().model
            # Check can_create only for trackable models
            if issubclass(model_class, TrackableModel):
                return has_model_perm and model_class.can_create(
                    request.user, request.data
                )

        return has_model_perm

    def has_object_read_permission(self, request, view, obj):
        has_model_perm = super(CustomPermissionSet, self).has_permission(request, view)
        user = request.user

        # Workaround for non trackable models
        if not isinstance(obj, TrackableModel):
            return has_model_perm

        return has_model_perm and (
            obj.created_by == user or obj.owner == user or obj.can_read(user)
        )

    def has_object_write_permission(self, request, view, obj):
        has_model_perm = super(CustomPermissionSet, self).has_permission(request, view)

        # Workaround for non trackable models
        if not isinstance(obj, TrackableModel):
            return has_model_perm

        user = request.user
        return has_model_perm and (
            obj.created_by == user or obj.owner == user or obj.can_write(user)
        )


class HasWriteAccess(permissions.BasePermission):
    """
    Allows individual access only Users with Write Access
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.can_write(request.user)
