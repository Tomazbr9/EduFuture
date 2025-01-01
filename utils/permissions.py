from rest_framework import permissions
from courses.models import StudentCourse, Student

class IsInstructor(permissions.BasePermission):
    """
    Permissão personalizada para verificar se o usuario é professor
    """
    def has_permission(self, request, view) -> bool | None:
        
        if request.user.is_authenticated:
            return hasattr(request.user, 'instructor')

# class PurchaseVerifition(permissions.BasePermission):

#     def has_permission(self, request, view):
#         user = request.user
#         student = Student.objects.get(user=user)
#         course = request.data.get('course')
        
#         if not StudentCourse.objects.get(student=student, course=course):
#             return False 