# Generated by Django 2.2.6 on 2020-03-06 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=120)),
                ('vname', models.CharField(max_length=120)),
                ('tx_hash', models.CharField(max_length=200)),
                ('block_hash', models.CharField(max_length=200)),
            ],
        ),
    ]