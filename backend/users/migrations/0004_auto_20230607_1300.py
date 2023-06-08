# Generated by Django 3.2.3 on 2023-06-07 10:00

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230607_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=150, validators=[users.validators.validate_first_last_name], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=150, validators=[users.validators.validate_first_last_name], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=64, verbose_name='Пароль'),
        ),
    ]