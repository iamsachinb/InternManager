# Generated by Django 4.2.9 on 2024-01-08 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_intern_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='intern',
            options={},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['regno']},
        ),
    ]
