from django.db import models

from DjangoUeditor.models import UEditorField

from users.models import BaseModel, UserProfile


class Cities(BaseModel):
    name = models.CharField(verbose_name="城市名", unique=True, max_length=100)
    desc = models.CharField(verbose_name="描述", default="", max_length=500)

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(BaseModel):
    user = models.OneToOneField(UserProfile, verbose_name="用户", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(verbose_name="机构名称", unique=True, max_length=100)
    desc = UEditorField(verbose_name="机构描述", width=580, height=400, imagePath="orgs/ueditor/images/",
                               filePath="orgs/ueditor/files/")
    tag = models.CharField(verbose_name="机构标签", default="全国知名", max_length=50)
    category = models.CharField(verbose_name="机构类别", default="培训机构", max_length=4,
                                choices=(("pxjg", "培训机构"), ("gr", "个人"), ("gx", "高校")))
    click_nums = models.IntegerField(verbose_name="点击数", default=0)
    fav_nums = models.IntegerField(verbose_name="收藏数", default=0)
    image = models.ImageField(verbose_name="logo", upload_to="org/images/%Y/%m", max_length=100)
    city = models.ForeignKey(Cities, verbose_name="城市", on_delete=models.CASCADE)
    address = models.CharField(verbose_name="机构地址", max_length=200)
    students = models.IntegerField(verbose_name="学习人数", default=0)
    course_nums = models.IntegerField(verbose_name="课程数", default=0)
    is_auth = models.BooleanField(verbose_name="是否认证", default=False)
    is_gold = models.BooleanField(verbose_name="是否金牌", default=False)

    # 获取对应机构下的课程
    def get_courses(self):
        courses = self.courses_set.filter(is_classic=True)[:3]
        return courses

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def show_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<img width=200px height=150px src='{}'>".format(self.image.url))
    show_image.short_description = "图片"

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='/org/{}'>跳转</a>".format(self.id))

    go_to.short_description = "跳转"


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
    image = models.ImageField(verbose_name="头像", upload_to="teacher/images/%Y/%m", max_length=100)
    is_auth = models.BooleanField(verbose_name="是否认证", default=False)
    is_gold = models.BooleanField(verbose_name="是否金牌", default=False)

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def course_nums(self):
        return self.courses_set.all().count()

    def __str__(self):
        return self.name

