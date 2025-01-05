from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentClass, StudentModule, StudentCourse

@receiver(post_save, sender=StudentClass)
def update_module_and_course_completion(sender, instance, **kwargs):
    student = instance.student
    cls = instance.cls
    module = cls.module
    course = module.course

    # Verificar se todas as aulas do módulo foram concluídas para o aluno
    all_classes_completed = module.classes.filter(
        studentclass__student=student,
        studentclass__completed=False
    ).count() == 0

    if all_classes_completed:
        # Marcar o módulo como concluído
        StudentModule.objects.update_or_create(
            student=student, module=module,
            defaults={'completed': True}
        )

    # Verificar se todos os módulos do curso foram concluídos para o aluno
    all_modules_completed = course.modules.filter(
        studentmodule__student=student,
        studentmodule__completed=False
    ).count() == 0

    if all_modules_completed:
        # Marcar o curso como concluído
        StudentCourse.objects.update_or_create(
            student=student, course=course,
            defaults={'completed': True}
        )
