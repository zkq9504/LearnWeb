from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse


from organizations.models import CourseOrg, Cities
from organizations.forms import AddAskForm


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
