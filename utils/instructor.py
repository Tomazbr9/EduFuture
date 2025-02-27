from courses.models import Student, Course, Module
from django.db.models import QuerySet

class InstructorUtil:
    
    def __init__(self, request) -> None:
        self.user = request.user

    def take_courses(self) -> QuerySet[Course] | None:
        courses = Course.objects.filter(instructor__user=self.user)
        return courses if courses.exists() else None
    
    def take_modules(self) -> QuerySet[Module] | None:
        modules = Module.objects.filter(course__instructor__user=self.user)
        return modules if modules.exists() else None