# Generated by Django 4.1.6 on 2023-07-17 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='availableinvestment',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='investmemt/'),
        ),
    ]