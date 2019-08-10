from django.db import models


# Create your models here.
from users.models import BaseModel
from organizations.models import Teachers


class Courses(BaseModel):
    teacher = models.ForeignKey(Teachers, verbose_name="讲师", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="课程名", max_length=100)
    desc = models.CharField(verbose_name="课程描述", max_length=500)
    degree = models.CharField(verbose_name="课程难度", choices=(("CJ", "初级"), ("ZJ", "中级"), ("GJ", "高级")), max_length=2)
    learn_times = models.IntegerField(verbose_name="学习时长（分钟数）", default=0,)
    students = models.IntegerField(verbose_name="学习人数", default=0)
    fav_nums = models.IntegerField(verbose_name="收藏人数", default=0)
    click_nums = models.IntegerField(verbose_name="点击数", default=0)
    category = models.CharField(verbose_name="课程类别", default="", max_length=30)
    tag = models.CharField(verbose_name="课程标签", default="", max_length=30)
    you_need_now = models.CharField(verbose_name="课程须知", default="", max_length=500)
    teacher_tell = models.CharField(verbose_name="老师告诉你", default="", max_length=500)

    detail = models.TextField(verbose_name="课程详情")
    image = models.ImageField(verbose_name="封面图", upload_to="courses/%Y/%m")

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lessons(BaseModel):
    course = models.ForeignKey(Courses, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="章节名", max_length=100)
    learn_times = models.IntegerField(verbose_name="学习时长（分钟数）", default=0,)

    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    lesson = models.ForeignKey(Lessons, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="视频名", max_length=100)
    learn_times = models.IntegerField(verbose_name="学习时长（分钟数）", default=0,)
    url = models.CharField(verbose_name="视频地址", max_length=200)

    class Meta:
        verbose_name = "课程视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(BaseModel):
    course = models.ForeignKey(Courses, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="名称", max_length=100)
    file = models.FileField(verbose_name="资源地址", upload_to="course/resource/%Y/%m", max_length=200)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name