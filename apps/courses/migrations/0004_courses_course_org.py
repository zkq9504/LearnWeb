# Generated by Django 2.2 on 2019-08-11 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0005_auto_20190811_1517'),
        ('courses', '0003_auto_20190811_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='course_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.CourseOrg', verbose_name='课程机构'),
        ),
    ]
