from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from courses.models import StudentCourse, Student

class IsInstructor(permissions.BasePermission):
    """
    Permissão personalizada para verificar se o usuario é professor 
    e dono do curso
    """
    def has_object_permission(self, request, view, obj):
        
        if not request.user.is_authenticated:
            return False
        
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return False
        
        
        try:
            course_or_module_get_instructor = obj.course.instructor
        except AttributeError:
            course_or_module_get_instructor = obj.instructor


        return course_or_module_get_instructor == student
     
    
class VerifyCoursePurchase(permissions.BasePermission):
    
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


