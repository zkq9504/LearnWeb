from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse


from organizations.models import CourseOrg, Cities
from organizations.forms import AddAskForm
from operations.models import UserFavorite


class OrgView(View):
    def get(self, request, *args, **kwargs):
        all_orgs = CourseOrg.objects.all()
        all_city = Cities.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        category = request.GET.get("ct", "")
        city_id = request.GET.get("city", "")
        # 根据机构类型分类
        if category:
            all_orgs = all_orgs.filter(category=category)
        # 根据所属城市分类
        if city_id:
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))
        # 根据学习人数或课程数排序
        sort = request.GET.get("sort")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")
        org_nums = all_orgs.count()
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, per_page=5, request=request)
        orgs = p.page(page)
        return render(request, 'org-list.html', {
                            "all_orgs": orgs,
                            "org_nums": org_nums,
                            "all_city": all_city,
                            "category": category,
                            "city_id": city_id,
                            "sort": sort,
                            "hot_orgs": hot_orgs,
        })


class AddAskView(View):
    def post(self, request, *args, **kwargs):
        ask_form = AddAskForm(request.POST)
        if ask_form.is_valid():
            ask_form.save(commit=True)
            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "提交失败，请检查后重新提交"
            })


class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        all_courses = course_org.courses_set.order_by("-students")[:3]
        all_teachers = course_org.teachers_set.order_by("-fav_nums")[:1]
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course_org.id):
                has_fav = True
        return render(request, "org-detail-homepage.html", {
             "course_org": course_org,
             "all_courses": all_courses,
             "all_teachers": all_teachers,
             "current_page": current_page,
             "has_fav": has_fav,
        })


class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.courses_set.order_by("-fav_nums")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=5, request=request)
        courses = p.page(page)
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course_org.id):
                has_fav = True
        return render(request, "org-detail-course.html", {
             "course_org": course_org,
             "all_courses": courses,
             "current_page": current_page,
             "has_fav": has_fav,
        })


class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course_org.id):
                has_fav = True
        return render(request, "org-detail-desc.html", {
             "course_org": course_org,
             "current_page": current_page,
             "has_fav": has_fav,
        })


class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teachers_set.order_by("-fav_nums")
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course_org.id):
                has_fav = True
        return render(request, "org-detail-teachers.html", {
             "course_org": course_org,
             "all_teachers": all_teachers,
             "current_page": current_page,
             "has_fav": has_fav,
        })
