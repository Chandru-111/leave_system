# Generated by Django 5.1.1 on 2024-12-10 13:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaveapplication',
            name='approved_by',
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='approved_or_rejected_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='current_holder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='holding_leaves', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='decision_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='forwarded_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]