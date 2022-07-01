# Generated by Django 3.2.7 on 2022-07-01 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0003_auto_20220629_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verdict', models.CharField(max_length=100)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('submission', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='problem',
            name='difficulty',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='Solution',
        ),
        migrations.AddField(
            model_name='submission',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.problem'),
        ),
    ]
