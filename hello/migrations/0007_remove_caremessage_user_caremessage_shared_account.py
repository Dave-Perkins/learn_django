# Generated by Django 5.2.3 on 2025-06-25 15:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0006_sharedaccount_customuser_shared_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caremessage',
            name='user',
        ),
        migrations.AddField(
            model_name='caremessage',
            name='shared_account',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='care_message', to='hello.sharedaccount'),
        ),
    ]
