# Generated by Django 4.0.3 on 2022-04-05 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UniversityProject', '0013_currencystock'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockchain',
            name='short',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
