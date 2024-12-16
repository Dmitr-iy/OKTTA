from rest_framework.permissions import BasePermission


class IsUserNotManager(BasePermission):
    """
    Ограничение доступа для менеджеров.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return not request.user.is_manager
