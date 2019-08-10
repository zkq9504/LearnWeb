from django.db import models
from django.contrib.auth import get_user_model

from users.models import BaseModel
from courses.models import Courses

UserProfile = get_user_model()


class UserAsk(BaseModel):
    name = models.CharField(verbose_name="姓名", max_length=50)
    mobile = models.CharField(verbose_name="手机", max_length=11)
    course_name = models.CharField(verbose_name="课程名称", max_length=50)

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name


class CourseComments(BaseModel):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, verbose_name="课程", on_delete=models.CASCADE)
    comments = models.CharField(verbose_name="评论", max_length=300)

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name


class UserFavorite(BaseModel):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    fav_id = models.IntegerField(verbose_name="数据id")
    fav_type = models.IntegerField(verbose_name="收藏类型", choices=((1, "课程"), (2, "课程机构"), (3, "讲师")))

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name


class UserMsg(BaseModel):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    message = models.CharField(verbose_name="消息内容", max_length=300)
    has_read = models.BooleanField(verbose_name="是否已读", default=False)

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name


class UserCourse(BaseModel):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, verbose_name="课程", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name