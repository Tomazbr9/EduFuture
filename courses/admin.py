from django.contrib import admin
from .models import Course, Module, Classe

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ['title', 'module']

