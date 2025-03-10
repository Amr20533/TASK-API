# Generated by Django 5.0.7 on 2025-01-06 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=250)),
                ('description', models.CharField(default='', max_length=1300)),
                ('priority', models.CharField(choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], default='low', max_length=60)),
                ('due_date', models.DateTimeField(max_length=90)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('inprogress', 'Inprogress'), ('finished', 'Finished')], default='pending', max_length=60)),
                ('image', models.ImageField(default='default_task.jpg', upload_to='task_images')),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
