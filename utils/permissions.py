from rest_framework import permissions
from courses.models import StudentCourse, Student

class IsInstructor(permissions.BasePermission):
    """
    Permissão personalizada para verificar se o usuário é professor.
    """

    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado
        if not request.user.is_authenticated:
            return False

        # Verifica se o usuário é um instrutor
        instructor = Student.objects.get(user=request.user)
        if hasattr(instructor, 'is_instructor') and instructor.is_instructor:
            return True

        # Caso contrário, nega permissão
        return False

    def has_object_permission(self, request, view, obj):
        # Verifica se o usuário está autenticado
        if not request.user.is_authenticated:
            return False
        
        # Obtém o instrutor do curso ou módulo
        try:
            course_or_module_get_instructor = obj.course.instructor
        except AttributeError:
            course_or_module_get_instructor = getattr(obj, 'instructor', None)

        if not course_or_module_get_instructor:
            return False

        # Verifica se o instrutor tem permissão
        return course_or_module_get_instructor.is_instructor


class VerifyCoursePurchase(permissions.BasePermission):

    def has_permission(self, request, view):
        ...
    
    def has_object_permission(self, request, view, obj):

        course = obj.module.course
        
        if not request.user.is_authenticated:
            return False
        
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return False
        
        if student.is_instructor:
            if course.instructor == student:
                return True
        
        if view.action in ['list', 'retrieve', 'partial_update']:
            return StudentCourse.objects.filter(student=student, course=course).exists()
        
        return False


