# Generated by Django 2.2 on 2019-08-11 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_courses_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='is_classic',
            field=models.BooleanField(default=False, verbose_name='是否经典'),
        ),
    ]