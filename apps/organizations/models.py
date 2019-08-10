from django.db import models

from users.models import BaseModel


class Cities(BaseModel):
    name = models.CharField(verbose_name="城市名", unique=True, max_length=100)
    desc = models.CharField(verbose_name="描述", default="", max_length=500)

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(BaseModel):
    name = models.CharField(verbose_name="机构名称", unique=True, max_length=100)
    desc = models.CharField(verbose_name="机构描述", max_length=500)
    tag = models.CharField(verbose_name="机构标签", default="全国知名", max_length=50)
    category = models.CharField(verbose_name="机构类别", default="培训机构", max_length=4,
                                choices=(("pxjg", "培训机构"), ("gr", "个人"), ("gx", "高校")))
    click_nums = models.IntegerField(verbose_name="点击数", default=0)
    fav_nums = models.IntegerField(verbose_name="收藏数", default=0)
    image = models.ImageField(verbose_name="logo", upload_to="org/%Y/%m", max_length=100)
    city = models.ForeignKey(Cities, verbose_name="城市", on_delete=models.CASCADE)
    address = models.CharField(verbose_name="机构地址", max_length=200)
    students = models.IntegerField(verbose_name="学习人数", default=0)
    course_nums = models.IntegerField(verbose_name="课程数", default=0)

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teachers(BaseModel):
    org = models.ForeignKey(CourseOrg, verbose_name="所在机构", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="姓名", max_length=100)
    age = models.IntegerField(verbose_name="年龄", default=20)
    work_years = models.IntegerField(verbose_name="工作年限", default=0)
    work_company = models.CharField(verbose_name="就职公司", max_length=100)
    work_position = models.CharField(verbose_name="公司职位", max_length=50)
    points = models.CharField(verbose_name="教学特点", max_length=50)
    click_nums = models.IntegerField(verbose_name="点击数", default=0)
    fav_nums = models.IntegerField(verbose_name="收藏人数", default=0)
    image = models.ImageField(verbose_name="头像", upload_to="teacher/%Y/%m", max_length=100)

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

