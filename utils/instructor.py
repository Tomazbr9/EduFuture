from courses.models import Student, Course, Module
from django.db.models import QuerySet

class InstructorUtil:
    
    def __init__(self, request) -> None:
        self.user = request.user
    
    # Funçao para obter todos os Cursos criados pelo instructor
    def take_courses(self) -> QuerySet[Course] | None:
        courses = Course.objects.filter(instructor__user=self.user)
        return courses if courses.exists() else None
    
    # Funçao para obter todos os modulos criados pelo instructor
    def take_modules(self) -> QuerySet[Module] | None:
        modules = Module.objects.filter(course__instructor__user=self.user)
        return modules if modules.exists() else None