# Generated by Django 5.1.1 on 2024-12-12 11:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_app', '0004_leaveapplication_votes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaveapplication',
            name='votes',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='current_holder',
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='approved_by',
            field=models.ForeignKey(blank=True, help_text='The user who approved the leave', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_leaves', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='current_holder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='holding_leaves', to=settings.AUTH_USER_MODEL),
        ),
    ]