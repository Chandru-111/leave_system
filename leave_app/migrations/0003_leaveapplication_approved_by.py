# Generated by Django 5.1.1 on 2024-12-10 13:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_app', '0002_remove_leaveapplication_approved_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveapplication',
            name='approved_by',
            field=models.ForeignKey(blank=True, help_text='The user who approved the leave', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_leaves', to=settings.AUTH_USER_MODEL),
        ),
    ]