# Generated by Django 4.0.3 on 2022-03-20 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Publication', '0006_linkedin_profile_info_associated_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkedin_account',
            name='message1',
            field=models.TextField(default=''),
        ),
    ]