from rest_framework import permissions
from courses.models import StudentCourse, Student

class IsInstructor(permissions.BasePermission):
    """
    Permissão personalizada para verificar se o usuario é professor
    """
    def has_permission(self, request, view) -> bool:
        
        if not request.user.is_authenticated:
            return False
        
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return False

        return student.is_instructor
        

        
class PurchaseVerifition(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        if not request.user.is_authenticated:
            return False
        
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return False
        
        if student.is_instructor:
            if obj.module.course.instructor == student:
                return True
        
            if view.action in ['list', 'retrieve', 'partial_update']:
                return True
            
            return False
        
        course = obj.module.course
        return StudentCourse.objects.filter(student=student, course=course).exists()


