# Generated by Django 2.2.6 on 2019-10-18 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=120)),
                ('location', models.CharField(max_length=50)),
                ('vote', models.IntegerField(default=0)),
            ],
        ),
    ]
