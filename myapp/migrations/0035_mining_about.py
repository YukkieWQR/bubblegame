# Generated by Django 4.2.13 on 2024-07-30 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0034_mining_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='mining',
            name='about',
            field=models.TextField(default='standart about text', max_length=50),
            preserve_default=False,
        ),
    ]