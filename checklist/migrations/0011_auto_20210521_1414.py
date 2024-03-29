# Generated by Django 3.1.7 on 2021-05-21 11:14

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0010_auto_20210521_1408'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='countries',
            new_name='country',
        ),
        migrations.RemoveField(
            model_name='drink',
            name='countries',
        ),
        migrations.AddField(
            model_name='drink',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
    ]
