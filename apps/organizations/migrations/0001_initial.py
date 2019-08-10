# Generated by Django 2.2 on 2019-08-07 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_basemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.BaseModel')),
                ('name', models.CharField(max_length=100, verbose_name='城市')),
                ('desc', models.CharField(default='', max_length=500, verbose_name='描述')),
            ],
            options={
                'verbose_name': '城市',
                'verbose_name_plural': '城市',
            },
            bases=('users.basemodel',),
        ),
        migrations.CreateModel(
            name='CourseOrg',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.BaseModel')),
                ('name', models.CharField(max_length=100, verbose_name='机构名称')),
                ('desc', models.CharField(max_length=500, verbose_name='机构描述')),
                ('tag', models.CharField(default='全国知名', max_length=50, verbose_name='机构标签')),
                ('category', models.CharField(choices=[('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')], default='培训机构', max_length=4, verbose_name='机构类别')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='收藏数')),
                ('image', models.ImageField(upload_to='org/%Y/%m', verbose_name='logo')),
                ('address', models.CharField(max_length=200, verbose_name='机构地址')),
                ('students', models.IntegerField(default=0, verbose_name='学习人数')),
                ('course_nums', models.IntegerField(default=0, verbose_name='课程数')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Cities')),
            ],
            options={
                'verbose_name': '课程机构',
                'verbose_name_plural': '课程机构',
            },
            bases=('users.basemodel',),
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.BaseModel')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('age', models.IntegerField(default=20, verbose_name='年龄')),
                ('work_years', models.IntegerField(default=0, verbose_name='工作年限')),
                ('work_company', models.CharField(max_length=100, verbose_name='就职公司')),
                ('work_position', models.CharField(max_length=50, verbose_name='公司职位')),
                ('points', models.CharField(max_length=50, verbose_name='教学特点')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='收藏人数')),
                ('image', models.ImageField(upload_to='teacher/%Y/%m', verbose_name='头像')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.CourseOrg', verbose_name='所在机构')),
            ],
            options={
                'verbose_name': '教师',
                'verbose_name_plural': '教师',
            },
            bases=('users.basemodel',),
        ),
    ]
