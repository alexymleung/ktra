# Generated by Django 4.2 on 2025-01-06 03:57

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=200)),
                ('amount', models.IntegerField()),
                ('donation_date', models.DateTimeField(default=datetime.datetime.now)),
                ('message', models.TextField(blank=True)),
                ('payment_type', models.CharField(max_length=200)),
                ('transaction_date', models.DateTimeField(default=datetime.datetime.now)),
                ('donor', models.ForeignKey(default=2, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
