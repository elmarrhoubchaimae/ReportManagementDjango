# Generated by Django 5.0.7 on 2024-07-31 14:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_register', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professeur',
            name='user',
        ),
        migrations.RemoveField(
            model_name='utilisateur',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='utilisateur',
            name='user_permissions',
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('student', 'Student'), ('professor', 'Professor')], max_length=10)),
                ('school_year', models.CharField(blank=True, choices=[('1', '1ère année'), ('2', '2ème année'), ('3', '3ème année')], max_length=2, null=True)),
                ('field', models.CharField(blank=True, choices=[('1', '2IA'), ('2', 'IDSIT'), ('3', 'IDF'), ('4', 'BI&A'), ('5', 'GL'), ('6', 'GD'), ('7', 'SSI'), ('8', 'SSE')], max_length=10, null=True)),
                ('department', models.CharField(blank=True, choices=[('1', '2IA'), ('2', 'IDSIT'), ('3', 'IDF'), ('4', 'BI&A'), ('5', 'GL'), ('6', 'GD'), ('7', 'SSI'), ('8', 'SSE')], max_length=10, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='rapport',
            name='user',
            field=models.ForeignKey(limit_choices_to={'user_type': 'student'}, on_delete=django.db.models.deletion.CASCADE, to='project_register.profile'),
        ),
        migrations.DeleteModel(
            name='Etudiant',
        ),
        migrations.DeleteModel(
            name='Professeur',
        ),
        migrations.DeleteModel(
            name='Utilisateur',
        ),
    ]
