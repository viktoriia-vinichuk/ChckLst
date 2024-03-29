# Generated by Django 3.1.7 on 2021-05-19 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0007_auto_20210516_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='books',
            field=models.ManyToManyField(blank=True, to='checklist.Book'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='drinks',
            field=models.ManyToManyField(blank=True, to='checklist.Drink'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='food',
            field=models.ManyToManyField(blank=True, to='checklist.Food'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='movies',
            field=models.ManyToManyField(blank=True, to='checklist.Movie'),
        ),
    ]
