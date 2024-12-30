from django.contrib import admin
from .models import Course, Module, Class, Category, Student, Instructor, StudentCourse

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['title', 'module']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'category']

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user', 'description', 'category']

@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'buy']