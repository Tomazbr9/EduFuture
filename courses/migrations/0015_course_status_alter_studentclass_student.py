# Generated by Django 5.1.4 on 2025-02-25 13:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_class_video_alter_class_materials_alter_course_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='studentclass',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_class', to='courses.student'),
        ),
    ]
