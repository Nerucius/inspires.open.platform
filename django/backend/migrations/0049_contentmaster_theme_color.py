# Generated by Django 2.2 on 2021-06-10 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0048_trackablemodel_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentmaster',
            name='theme_color',
            field=models.CharField(default='white', max_length=128),
        ),
    ]
