# Generated by Django 2.2.6 on 2019-10-16 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='pincode',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
