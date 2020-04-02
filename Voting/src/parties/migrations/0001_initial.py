# Generated by Django 2.2.6 on 2019-10-18 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('candidates', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=120)),
                ('members', models.ManyToManyField(blank=True, to='candidates.candidate')),
            ],
        ),
    ]