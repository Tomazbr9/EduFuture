from django.contrib import admin
from .models import Course, Module, Class

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['title', 'module']

