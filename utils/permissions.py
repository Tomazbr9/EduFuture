from rest_framework import permissions

class IsInstructor(permissions.BasePermission):
    """
    Permissão personalizada para verificar se o usuario é professor
    """
    def has_permission(self, request, view) -> bool | None:
        
        if request.user.is_authenticated:
            return hasattr(request.user, 'instructor')

