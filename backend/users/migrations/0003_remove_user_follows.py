# Generated by Django 3.2.3 on 2023-06-24 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_follows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='follows',
        ),
    ]