# Generated by Django 5.1.4 on 2025-01-25 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_alter_course_objective'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='image',
            field=models.ImageField(default='profiles/sem_perfil.jpg', upload_to='profiles'),
        ),
    ]
