# Generated by Django 5.1.4 on 2025-01-01 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_studentcourse_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='registered',
        ),
        migrations.AddField(
            model_name='course',
            name='certificate',
            field=models.URLField(blank=True),
        ),
    ]
