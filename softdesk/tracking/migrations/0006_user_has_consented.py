# Generated by Django 5.1.3 on 2024-12-29 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0005_rename_creator_issue_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_consented',
            field=models.BooleanField(default=False),
        ),
    ]
