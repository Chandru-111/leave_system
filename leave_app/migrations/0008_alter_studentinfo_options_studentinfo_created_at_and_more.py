# Generated by Django 5.1.1 on 2024-12-12 12:43

import django.utils.timezone
import leave_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_app', '0007_studentinfo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studentinfo',
            options={'verbose_name': 'Student Info', 'verbose_name_plural': 'Student Infos'},
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='aadhar_no',
            field=models.CharField(max_length=12, unique=True, validators=[leave_app.models.validate_aadhar_no]),
        ),
    ]