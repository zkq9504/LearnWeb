import xadmin

from organizations.models import CourseOrg, Cities, Teachers
from xadmin.layout import Fieldset, Main, Side, Row, FormHelper


class CourseOrgAdmin(object):
    list_display = ["name", "city", "address", "show_image", "go_to", "category", "tag", "course_nums", "students", "click_nums", "fav_nums", "add_time"]
    search_fields = ["name", "desc", "tag", "category", "city", "address"]
    list_filter = ["name", "tag", "category", "click_nums", "fav_nums", "city", "students", "course_nums", "add_time"]
    list_editable = ["name", "desc", "tag", "category", "city", "address"]
    style_fields = {
        "desc": "ueditor"
    }
    # 配置只读字段
    readonly_fields = ["click_nums", "fav_nums", "add_time", "students"]
    # 去除字段
    exclude = []
    # 按收藏数排序
    ordering = ["-fav_nums"]
    # 设置图标
    model_icon = "fa fa-book"

    def get_form_layout(self):
        self.form_layout = (
            Main(
                Fieldset("基本信息",
                         'name',
                         'city',
                         'address',
                         'category',
                         'tag',
                         css_class='unsort no_title'
                         ),
            ),
            Side(
                Fieldset("选择信息",
                         'is_auth',
                         'is_gold'
                         ),
                Fieldset("访问信息",
                         'click_nums',
                         'fav_nums',
                         'students'),
            )
        )
        return super(CourseOrgAdmin, self).get_form_layout()

    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        return qs


class CitiesAdmin(object):
    list_display = ["id", "name", "desc", "add_time"]
    search_fields = ["name", "desc",]
    list_filter = ["name", "desc", "add_time"]
    list_editable = ["name", "desc"]


class TeachersAdmin(object):
    list_display = ["id", "org", "name", "age", "work_company", "work_years", "points", "add_time"]
    search_fields = ["org", "name", "work_company", "points"]
    list_filter = ["org__name", "name", "age", "work_years", "work_company", "points", "click_nums", "fav_nums", "add_time"]
    list_editable = ["org", "name", "age", "work_years", "work_company", "points"]


xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Cities, CitiesAdmin)
xadmin.site.register(Teachers, TeachersAdmin)
