# Generated by Django 4.0.4 on 2022-07-04 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0010_alter_submission_submission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='submission',
            field=models.FilePathField(path='C:\\users\\pilla\\oj\\oj\\submissions'),
        ),
    ]
