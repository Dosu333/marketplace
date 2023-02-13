# Generated by Django 4.1.6 on 2023-02-13 13:37

from django.conf import settings
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableInvestment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=225)),
                ('interest_rate', models.IntegerField()),
                ('investment', models.IntegerField()),
                ('max_earning', models.IntegerField()),
                ('investment_duration', models.IntegerField()),
                ('investors', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]