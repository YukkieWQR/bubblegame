# Generated by Django 5.1 on 2024-09-24 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_userprofile_user_firstname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='last_12h_task',
            new_name='last_12h_task_1',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_12h_task_2',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
