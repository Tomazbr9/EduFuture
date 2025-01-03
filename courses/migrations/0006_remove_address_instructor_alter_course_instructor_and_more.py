# Generated by Django 5.1.4 on 2025-01-03 10:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_remove_course_registered_course_certificate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='instructor',
        ),
        migrations.AlterField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='courses.student'),
        ),
        migrations.RemoveField(
            model_name='student',
            name='courses',
        ),
        migrations.AddField(
            model_name='student',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='student',
            name='is_instructor',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Instructor',
        ),
    ]
