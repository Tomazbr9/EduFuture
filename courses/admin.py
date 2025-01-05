from django.contrib import admin
from .models import (Course, Module, Class, Category,
Student, StudentCourse, StudentModule, StudentClass)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'course']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'module']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'category', 'is_instructor']

@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course']

@admin.register(StudentModule)
class StudentModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'module']

@admin.register(StudentClass)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'cls']