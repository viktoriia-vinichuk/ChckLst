# Generated by Django 3.1.7 on 2021-05-06 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0004_choice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='b_genre',
            options={'ordering': ['genre']},
        ),
        migrations.AlterModelOptions(
            name='d_kind',
            options={'ordering': ['drink_kind']},
        ),
        migrations.AlterModelOptions(
            name='f_kind',
            options={'ordering': ['food_kind']},
        ),
        migrations.AlterModelOptions(
            name='m_genre',
            options={'ordering': ['genre']},
        ),
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
