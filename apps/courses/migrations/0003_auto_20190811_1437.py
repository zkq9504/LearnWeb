# Generated by Django 2.2 on 2019-08-11 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20190807_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='image',
            field=models.ImageField(upload_to='courses/images/%Y/%m', verbose_name='封面图'),
        ),
    ]