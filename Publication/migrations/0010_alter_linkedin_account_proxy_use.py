# Generated by Django 4.0.3 on 2022-03-22 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Publication', '0009_linkedin_account_proxy_host_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkedin_account',
            name='proxy_use',
            field=models.BooleanField(default=False),
        ),
    ]