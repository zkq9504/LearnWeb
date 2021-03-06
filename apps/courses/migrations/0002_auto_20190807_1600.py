# Generated by Django 2.2 on 2019-08-07 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseresource',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Courses', verbose_name='课程'),
        ),
        migrations.AlterField(
            model_name='lessons',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Courses', verbose_name='课程'),
        ),
    ]
