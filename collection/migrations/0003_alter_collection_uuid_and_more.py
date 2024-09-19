# Generated by Django 5.1.1 on 2024-09-17 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0002_collection_user_alter_moviesincollection_collection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='uuid',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='moviesincollection',
            name='movie_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]