# Generated by Django 3.1.7 on 2021-05-19 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0008_auto_20210519_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(blank=True, to='checklist.B_Genre'),
        ),
        migrations.AlterField(
            model_name='drink',
            name='drink_kinds',
            field=models.ManyToManyField(blank=True, to='checklist.D_kind'),
        ),
        migrations.AlterField(
            model_name='food',
            name='food_kinds',
            field=models.ManyToManyField(blank=True, to='checklist.F_Kind'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(blank=True, to='checklist.M_Genre'),
        ),
    ]
