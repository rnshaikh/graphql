# Generated by Django 4.2.5 on 2023-09-24 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_groups_user_is_superuser_user_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
