# Generated by Django 4.0.4 on 2022-07-04 17:38

from django.db import migrations, models
import judge.models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0014_alter_submission_submission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='submission',
            field=models.FilePathField(max_length=255, path=judge.models.submission_path),
        ),
    ]