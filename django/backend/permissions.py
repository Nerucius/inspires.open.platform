from rest_framework import permissions


class CustomPermissionSet(permissions.DjangoModelPermissions):
    """ Custom application logic Permissions. Premise is user MUST
        be logged in for any kind of permission.
        Runs the DjangoModelPermissions schema first so that
        group permissions work.
    """

    CREATE_METHOD = "POST"

    def has_permission(self, request, view):
        # Next line skips views without a queryset (API root)
        if not hasattr(view, "get_queryset"):
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return self.has_read_permission(request, view)
        return self.has_write_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return self.has_object_read_permission(request, view, obj)
        return self.has_object_write_permission(request, view, obj)

    def has_read_permission(self, request, view):
        # print("has_read_permission", request.user, view.get_queryset().model)
        return True

    def has_write_permission(self, request, view):
        # print("has_write_permission", request.user, view.get_queryset().model)
        # Return default Django model permissions for WRITE unsafe methods
        has_model_perm = super(CustomPermissionSet, self).has_permission(request, view)
        model_class = view.get_queryset().model
        if request.method == self.CREATE_METHOD:
            return has_model_perm and model_class.can_create(request.user, request.data)
        return has_model_perm

    def has_object_read_permission(self, request, view, obj):
        # print("has_object_read_permission", request.user, obj)
        user = request.user
        return obj.created_by == user or obj.owner == user or obj.can_read(user)

    def has_object_write_permission(self, request, view, obj):
        # print("has_object_write_permission", request.user, obj)
        user = request.user
        return obj.created_by == user or obj.owner == user or obj.can_write(user)
