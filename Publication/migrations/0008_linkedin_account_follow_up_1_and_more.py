# Generated by Django 4.0.3 on 2022-03-21 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Publication', '0007_linkedin_account_message1'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkedin_account',
            name='follow_up_1',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='linkedin_account',
            name='follow_up_2',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='linkedin_account',
            name='follow_up_3',
            field=models.TextField(default=''),
        ),
    ]
