# Generated by Django 5.1.4 on 2025-01-03 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_remove_address_instructor_alter_course_instructor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
