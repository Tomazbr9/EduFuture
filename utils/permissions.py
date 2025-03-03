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
    """
    Permissão personalizada para verificar se o usuário comprou o curso antes de acessar o conteúdo.
    """

    def has_permission(self, request, view):
        """
        Verifica se o usuário está autenticado antes de permitir qualquer acesso.
        """
        if not request.user.is_authenticated:
            raise PermissionDenied('É necessário estar autenticado')  # Bloqueia acesso de usuários não autenticados
        return True

    def has_object_permission(self, request, view, obj):
        """
        Verifica se o usuário tem permissão para acessar um objeto específico (curso).
        """
        # Obtém o curso associado ao objeto acessado
        course = obj.module.course

        try:
            # Busca o estudante vinculado ao usuário logado
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return False  # Se o usuário não for um estudante, nega o acesso

        # Permite acesso caso o usuário seja o instrutor do curso
        if student.is_instructor and course.instructor == student:
            return True

        # Se a ação for listar ou visualizar ('list', 'retrieve'), verifica se o aluno comprou o curso
        if getattr(view, "action", None) in ['list', 'retrieve']:
            if not StudentCourse.objects.filter(student=student, course=course).exists():
                # Se o aluno não comprou o curso, bloqueia o acesso
                raise PermissionDenied('É necessário comprar o curso para assistir às aulas!')
            return True  # Permite o acesso se o aluno tiver comprado o curso

        return False  # Caso nenhuma condição seja atendida, nega o acesso