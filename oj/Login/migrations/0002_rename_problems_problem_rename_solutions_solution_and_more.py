# Generated by Django 4.0.4 on 2022-06-27 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Problems',
            new_name='Problem',
        ),
        migrations.RenameModel(
            old_name='Solutions',
            new_name='Solution',
        ),
        migrations.RenameModel(
            old_name='TestCases',
            new_name='TestCase',
        ),
    ]
