# Generated by Django 2.2.6 on 2019-10-18 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0002_candidate_affiliation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='cname',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='location',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
