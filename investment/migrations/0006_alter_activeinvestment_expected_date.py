# Generated by Django 4.1.6 on 2023-09-08 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0005_rename_investment_availableinvestment_investment_duration_in_days_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activeinvestment',
            name='expected_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
