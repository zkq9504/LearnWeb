from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
import redis

from pure_pagination import Paginator, PageNotAnInteger

from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm, RegisterPostForm
from apps.users.forms import ImageUploadForm, InfoForm, UpdatePwdForm, UpdateMobileForm
from apps.utils.YunPian import send_verify_sms
from apps.utils.random_str import generate_random
from users.models import UserProfile
from operations.models import UserFavorite, UserMsg
from organizations.models import CourseOrg, Teachers
from courses.models import Courses
from LearnOnline.settings import REDIS_HOST, REDIS_PORT


class LoginView(View):
    """用户登录"""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()
        return render(request, "login.html", {"login_form": login_form, "next": next})

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=password)
            if user is not None:
                login(request, user)
                next = request.GET.get("next", "")
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误", "login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})


class DynamicLoginView(View):
    """用户手机号登录"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()
        return render(request, "login.html", {"login_form": login_form, "next": next})
    def post(self,request):
        login_form = DynamicLoginPostForm
        dynamic_login = True
        if login_form.is_valid():
            mobile = login_form.cleaned_data["mobile"]
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                user = UserProfile(username=mobile)
                password = generate_random(10, 1)
                user.set_password(password)
                user.mobile = mobile
            login(request, user)
            next = request.GET.get("next", "")
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse("index"))
        else:
            d_form = DynamicLoginForm()
            return render(request, "login.html", {"login_form": login_form,
                                                  "d_form": d_form,
                                                  "dynamic_login": dynamic_login})


class RegisterView(View):
    """用户注册"""
    def get(self, request):
        register_get_form = RegisterGetForm()
        return render(request, "register.html", {"register_get_form": register_get_form})
    def post(self, request):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]
            user = UserProfile(username=mobile)
            user.mobile = mobile
            user.set_password(password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            register_get_form = RegisterGetForm()
            return render(request, "register.html", {
                "register_get_form": register_get_form,
                "register_post_form": register_post_form})


class LogoutView(View):
    """用户登出"""
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class SendSmsView(View):
    """发送短信验证码"""
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data["mobile"]
            code = generate_random(4, 0)
            re_json = send_verify_sms()
            if re_json["code"] == 0:
                re_dict["status"] = "success"
                db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
                db.set(str(mobile), code)
                db.expire(mobile, 60*3)
            else:
                re_dict["msg"] = re_json["msg"]
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]

        return JsonResponse(re_dict)


class UserInfoView(LoginRequiredMixin, View):
    """用户个人信息"""
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        captcha_form = RegisterGetForm()
        return render(request, "usercenter-info.html", {"captcha_form": captcha_form, "current_page": "info"})

    def post(self, request, *args, **kwargs):
        info_form = InfoForm(request.POST, instance=request.user)
        if info_form.is_valid():
            info_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({info_form.errors})


class ImageUploadView(LoginRequiredMixin, View):
    """用户更改头像"""
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        image_upload_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if image_upload_form.is_valid():
            image_upload_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })


class UpdatePwdView(LoginRequiredMixin, View):
    """用户更改登录密码"""
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        pwd_form = UpdatePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd = pwd_form.cleaned_data["password1"]
            user = request.user
            user.set_password(pwd)
            user.save()
            # login(request, user)
            return JsonResponse({
                "status": "success"
            })

        else:
            return JsonResponse(pwd_form.errors)


class UpdateMobileView(LoginRequiredMixin, View):
    """用户更改手机号"""
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        mobile_form = UpdateMobileForm(request.POST)
        if mobile_form.is_valid():
            mobile = mobile_form.cleaned_data["mobile"]
            if UserProfile.objects.filter(mobile=mobile):
                return JsonResponse({
                    "mobile": "该手机号已注册"
                })
            user = request.user
            user.mobile = mobile
            user.username = mobile
            user.save()
            # logout(request)
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(mobile_form.errors)


class MyCourseView(LoginRequiredMixin, View):
    """用户课程视图"""
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        return render(request, "usercenter-mycourse.html", {"current_page": "mycourse"})


class MyFavoriteView(LoginRequiredMixin, View):
    """用户收藏视图"""
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        sort = request.GET.get("sort", "")
        if sort == "":
            orgs = []
            user_favs = UserFavorite.objects.filter(user=request.user, fav_type=2)
            for user_fav in user_favs:
                org = CourseOrg.objects.get(id=user_fav.fav_id)
                orgs.append(org)
            return render(request, "usercenter-myfavorite.html", {
                "orgs": orgs,
                "sort": sort,
                "current_page": "myfavorite",
            })

        elif sort == "teacher":
            teachers = []
            user_favs = UserFavorite.objects.filter(user=request.user, fav_type=3)
            for user_fav in user_favs:
                teacher = Teachers.objects.get(id=user_fav.fav_id)
                teachers.append(teacher)
            return render(request, "usercenter-myfavorite.html", {
                "teachers": teachers,
                "sort": sort,
                "current_page": "myfavorite",
            })

        elif sort == "course":
            courses = []
            user_favs = UserFavorite.objects.filter(user=request.user, fav_type=1)
            for user_fav in user_favs:
                course = Courses.objects.get(id=user_fav.fav_id)
                courses.append(course)
            return render(request, "usercenter-myfavorite.html", {
                "courses": courses,
                "sort": sort,
                "current_page": "myfavorite",
            })


class MyMessageView(LoginRequiredMixin, View):
    """用户消息视图"""
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        all_messages = UserMsg.objects.filter(user=request.user)
        for message in all_messages:
            message.has_read = True
            message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, per_page=3, request=request)
        messages = p.page(page)
        return render(request, "usercenter-message.html", {"messages": messages, "current_page": "mymessage"})


def msg_nums(request):
    if request.user.is_authenticated:
        unread_msgnums = UserMsg.objects.filter(user=request.user, has_read=False).count()
        return {'unread_msgnums': unread_msgnums}
    else:
        return {}
