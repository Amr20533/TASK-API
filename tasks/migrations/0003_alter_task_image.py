# Generated by Django 5.0.7 on 2025-01-08 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='image',
            field=models.ImageField(default='task_images/default_task.jpg', upload_to='task_images'),
        ),
    ]
