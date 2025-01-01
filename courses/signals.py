from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Class


@receiver(post_save, sender=Class)
def check_complete_modules(sender, instance, **kwargs):
    
    module = instance.module

    if module.classes.filter(completed=False).count() == 0:
        module.completed = True
        module.save()
        check_complete_courses(module.course)

def check_complete_courses(course):

    if course.modules.filter(completed=False).count() == 0:
        course.completed = True
        course.save()