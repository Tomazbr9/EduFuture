from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from courses.models import StudentCourse, Student

class IsInstructor(permissions.BasePermission):
    """
    Permissão personalizada para verificar se o usuário é professor.
    """

    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado
        if not request.user.is_authenticated:
            return PermissionDenied('É necessario está logado para assistir as aulas')

        # Verifica se o usuário é um instrutor
        instructor = Student.objects.get(user=request.user)
        if hasattr(instructor, 'is_instructor') and instructor.is_instructor:
            return True

        # Caso contrário, nega permissão
        return PermissionDenied('Somente professores podem executar essa ação')

    def has_object_permission(self, request, view, obj):
        # Obtém o instrutor do curso ou módulo
        try:
            course_or_module_get_instructor = obj.course.instructor
        except AttributeError:
            course_or_module_get_instructor = getattr(obj, 'instructor', None)

        if not course_or_module_get_instructor:
            return False

        # Verifica se o instrutor tem permissão
        if course_or_module_get_instructor.is_instructor:
            if course_or_module_get_instructor.user != request.user:
                raise PermissionDenied("Não é possivel editar informaçoes dos cursos de outros professores!!")
            else:
                return True


class VerifyCoursePurchase(permissions.BasePermission):

    def has_permission(self, request, view):
        
        if not request.user.is_authenticated:
            raise PermissionDenied('É necessario está autenticado')
        
        return True
    
    def has_object_permission(self, request, view, obj):

        course = obj.module.course
        
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return False
        
        if student.is_instructor:
            if course.instructor == student:
                return True
        
        if view.action in ['list', 'retrieve', 'partial_update']:
            if not StudentCourse.objects.filter(student=student, course=course).exists():
                raise PermissionDenied('É necessario comprar o curso para assistir as aulas!')
            else:
                return True
        
        # if obj.module.course.instructor.user == request.user:
        #     return True
        


