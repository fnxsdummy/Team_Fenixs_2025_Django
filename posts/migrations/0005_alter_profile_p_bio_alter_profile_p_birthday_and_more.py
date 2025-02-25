# Generated by Django 5.1.2 on 2024-11-16 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_rename_p_user_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='p_bio',
            field=models.TextField(blank=True, default='Add your Bio', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='p_birthday',
            field=models.DateField(blank=True, default='2000-01-01', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='p_gender',
            field=models.TextField(blank=True, default='Add your Gender', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='p_phone',
            field=models.TextField(blank=True, default='Add your Number', null=True),
        ),
    ]
