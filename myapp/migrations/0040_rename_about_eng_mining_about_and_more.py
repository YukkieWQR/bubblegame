# Generated by Django 4.2.13 on 2024-08-10 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0039_rename_about_mining_about_eng_mining_about_rus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mining',
            old_name='about_eng',
            new_name='about',
        ),
        migrations.RenameField(
            model_name='mining',
            old_name='name_eng',
            new_name='name',
        ),
    ]