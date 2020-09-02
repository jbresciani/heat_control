# Generated by Django 3.1.1 on 2020-09-02 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Thermostats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('group', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('url', models.CharField(max_length=128)),
                ('current_temp', models.IntegerField(default=14)),
                ('requested_temp', models.IntegerField(default=14)),
            ],
        ),
    ]