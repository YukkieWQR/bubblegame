# Generated by Django 4.2.13 on 2024-07-14 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_task_taskuser_delete_tasks_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='referral',
            name='invited',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='referral',
            name='referrer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userprofile'),
        ),
        migrations.AlterField(
            model_name='referral',
            name='token',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='users_invited',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]