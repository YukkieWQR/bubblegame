# Generated by Django 4.2.13 on 2024-07-25 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_alter_mining_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='picture',
            field=models.ImageField(upload_to='myapp/static/task_pictures/'),
        ),
    ]