from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


GENDER_CHOICES = (
    ("male", "男"),
    ("female", "女")
)


class BaseModel(models.Model):
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        abstract: True


class UserProfile(AbstractUser):
    nick_name = models.CharField(verbose_name="昵称", max_length=50, default="")
    gender = models.CharField(verbose_name="性别", max_length=6, choices=GENDER_CHOICES)
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    address = models.CharField(verbose_name="地址", max_length=100, default="")
    mobile = models.CharField(verbose_name="号码", max_length=11)
    image = models.ImageField(verbose_name="用户头像", upload_to="head_image/%Y/%m", default="head_image/default.jpg")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username