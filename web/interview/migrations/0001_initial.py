# Generated by Django 2.1.2 on 2018-10-08 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='difficulty_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'interview_difficulty',
            },
        ),
        migrations.CreateModel(
            name='language_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('lname', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'interview_language',
            },
        ),
        migrations.CreateModel(
            name='problem_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('time_limit', models.IntegerField()),
                ('memory_limit', models.IntegerField()),
                ('test_case_info', models.TextField()),
                ('can_exam', models.BooleanField()),
                ('difficulty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interview.difficulty_model')),
                ('languages', models.ManyToManyField(to='interview.language_model')),
            ],
            options={
                'db_table': 'interview_problem',
            },
        ),
        migrations.CreateModel(
            name='tag_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'interview_tag',
            },
        ),
        migrations.AddField(
            model_name='problem_model',
            name='tags',
            field=models.ManyToManyField(to='interview.tag_model'),
        ),
    ]
