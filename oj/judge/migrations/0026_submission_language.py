# Generated by Django 3.2.7 on 2022-07-04 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0025_auto_20220705_0125'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='language',
            field=models.CharField(choices=[('cpp', 'C++'), ('java', 'Java'), ('python', 'Python')], default='cpp', max_length=255),
        ),
    ]
