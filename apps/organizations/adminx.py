import xadmin

from organizations.models import CourseOrg, Cities, Teachers


class CourseOrgAdmin(object):
    list_display = ["id", "name", "city", "address",  "category", "tag", "course_nums", "students", "click_nums", "fav_nums", "add_time"]
    search_fields = ["name", "desc", "tag", "category", "city", "address"]
    list_filter = ["name", "tag", "category", "click_nums", "fav_nums", "city", "students", "course_nums", "add_time"]
    list_editable = ["name", "desc", "tag", "category", "city", "address"]


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
