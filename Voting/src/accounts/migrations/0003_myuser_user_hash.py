# Generated by Django 2.2.6 on 2020-03-06 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20191016_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='user_hash',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]