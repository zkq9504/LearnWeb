from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from operations.models import UserFavorite, CourseComments
from courses.models import Courses
from organizations.models import CourseOrg, Teachers
from apps.operations.forms import UserFavForm, CommentForm


class AddFavView(View):
    def post(self, request, *args, **kwargs):
        """用户收藏、取消收藏"""
        # 判断用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })
        user_fav_form = UserFavForm(request.POST)
        # 判断表单是否有效
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data["fav_id"]
            fav_type = user_fav_form.cleaned_data["fav_type"]
            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if existed_records:
                existed_records.delete()
                if fav_type == 1:
                    course = Courses.objects.get(id=fav_id)
                    course.fav_nums -=1
                    course.save()
                elif fav_type == 2:
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_nums -= 1
                    org.save()
                elif fav_type == 3:
                    teacher = Teachers.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()
                return JsonResponse({
                    "status": "success",
                    "msg": "收藏"
                })
            else:
                if fav_type == 1:
                    course = Courses.objects.get(id=fav_id)
                    course.fav_nums +=1
                    course.save()
                elif fav_type == 2:
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_nums += 1
                    org.save()
                elif fav_type == 3:
                    teacher = Teachers.objects.get(id=fav_id)
                    teacher.fav_nums += 1
                    teacher.save()
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()
                return JsonResponse({
                    "status": "success",
                    "msg": "已收藏"
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数有误"
            })


class CommentView(View):
    def post(self, request, *args, **kwargs):
        """用户评论"""
        # 判断用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = CourseComments()
            comment.user = request.user
            comment.course = comment_form.cleaned_data["course"]
            comment.comments = comment_form.cleaned_data["comments"]
            comment.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "评论出错，请重新评论"
            })

