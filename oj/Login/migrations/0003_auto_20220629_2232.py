# Generated by Django 3.2.7 on 2022-06-29 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0002_rename_problems_problem_rename_solutions_solution_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='solution_file',
            field=models.TextField(default='Enter code'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='difficulty',
            field=models.IntegerField(help_text='Enter your solution'),
        ),
    ]
