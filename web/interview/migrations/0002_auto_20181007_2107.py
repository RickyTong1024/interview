# Generated by Django 2.1.2 on 2018-10-07 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='difficulty_model',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='language_model',
            name='lname',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='language_model',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='problem_model',
            name='title',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='tag_model',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]