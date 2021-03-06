# Generated by Django 4.0.4 on 2022-07-04 22:22

from django.db import migrations, models
import judge.models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0026_submission_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='input',
            field=models.FilePathField(max_length=255, path=judge.models.testcase_input),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='output',
            field=models.FilePathField(max_length=255, path=judge.models.testcase_output),
        ),
    ]
