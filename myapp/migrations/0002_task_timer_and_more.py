# Generated by Django 5.0.3 on 2024-08-22 16:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task_Timer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('picture', models.ImageField(upload_to='myapp/static/task_pictures/')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='daily_energy_last_daily_bonus',
            new_name='last_12h_task',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='daily_turbo_last_daily_bonus',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_energy_update',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_mining_bonus',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='recieved_threefriends_reward',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='TaskUser_Timer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Start'), (2, 'Claim'), (3, 'Done')], default=1)),
                ('timer', models.DateTimeField(blank=True, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userprofile')),
            ],
        ),
    ]
