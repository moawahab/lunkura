# Generated by Django 4.0.2 on 2022-09-20 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(default='coding', max_length=225),
        ),
    ]