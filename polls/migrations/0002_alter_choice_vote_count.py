# Generated by Django 4.2.5 on 2023-09-11 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='vote_count',
            field=models.IntegerField(default=0),
        ),
    ]