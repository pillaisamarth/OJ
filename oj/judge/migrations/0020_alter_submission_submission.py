# Generated by Django 3.2.7 on 2022-07-04 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0019_alter_submission_submission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='submission',
            field=models.FilePathField(max_length=255, path='C:\\users\\pilla\\oj\\oj\\Submissions', recursive=True),
        ),
    ]
