from django import forms
import redis

from captcha.fields import CaptchaField

from LearnOnline.settings import REDIS_HOST, REDIS_PORT
from users.models import UserProfile


class LoginForm(forms.Form):
    """用户名登录表单验证"""
    username = forms.CharField(required=True, min_length=2, max_length=30)
    password = forms.CharField(required=True, min_length=6, max_length=20)


class DynamicLoginForm(forms.Form):
    """动态登录手机号及图片验证码表单验证"""
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    captcha = CaptchaField()


class DynamicLoginPostForm(forms.Form):
    """动态登录手机号及短信验证码表单验证"""
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")

        db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = db.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码错误")
        return self.cleaned_data

    # def clean(self):
    #     mobile = self.cleaned_data["mobile"]
    #     code = self.cleaned_data["code"]
    #
    #     db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset="utf8", decode_responses=True)
    #     redis_code = db.get(str(mobile))
    #     if code != redis_code:
    #         raise forms.ValidationError("验证码错误")
    #     return self.cleaned_data


class RegisterGetForm(forms.Form):
    """图片验证码表单验证"""
    captcha = CaptchaField()


class RegisterPostForm(forms.Form):
    """注册表单验证"""
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)
    password = forms.CharField(required=True, min_length=6, max_length=20)

    def clean_mobile(self):
        mobile = self.data.get("mobile")
        user = UserProfile.objects.filter(mobile=mobile)
        if user:
            raise forms.ValidationError("该手机号已注册")
        return mobile

    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = db.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码错误")
        return code


class ImageUploadForm(forms.ModelForm):
    """用户更改头像表单验证"""
    class Meta:
        model = UserProfile
        fields = ["image"]


class InfoForm(forms.ModelForm):
    """用户更改个人信息表单验证"""
    class Meta:
        model = UserProfile
        fields = ["nick_name", "birthday", "gender", "address"]


class UpdatePwdForm(forms.Form):
    """用户更改密码表单验证"""
    password1 = forms.CharField(required=True, min_length=6, max_length=20)
    password2 = forms.CharField(required=True, min_length=6, max_length=20)

    def clean(self):
        pwd1 = self.cleaned_data["password1"]
        pwd2 = self.cleaned_data["password2"]
        if pwd1 != pwd2:
            raise forms.ValidationError("两次输入的密码不一致")
        return self.cleaned_data


class UpdateMobileForm(forms.Form):
    """用户更改手机号时手机号及短信验证码表单验证"""
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")

        db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = db.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码错误")
        return self.cleaned_data