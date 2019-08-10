import xadmin

from courses.models import Courses, Lessons, Video, CourseResource


class GlobalSettings(object):
    site_title = "学习在线后台管理系统"
    site_footer = "学习在线"
    # menu_style = "accordion"


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class CoursesAdmin(object):
    list_display = ["id", "name", "teacher", "category", "tag", "degree", "learn_times", "add_time"]
    search_fields = ["teacher", "name", "desc", "degree", "learn_times", "students", "fav_nums", "click_nums",
                     "category", "tag", "you_need_now", "teacher_tell"]
    list_filter = ["teacher__name", "name", "degree", "learn_times", "students", "fav_nums", "click_nums", "category", "tag", "add_time"]
    list_editable = ["teacher", "name", "desc", "degree", "learn_times", "category", "tag"]


class LessonsAdmin(object):
    list_display = ["id", "course", "name", "learn_times", "add_time"]
    search_fields = ["course", "name", "learn_times"]
    list_filter = ["course", "name", "learn_times", "add_time"]
    list_editable = ["course", "name", "learn_times"]


class VideoAdmin(object):
    list_display = ["id", "lesson", "name", "learn_times", "url", "add_time"]
    search_fields = ["lesson", "name", "learn_times", "url"]
    list_filter = ["lesson", "name", "learn_times", "url", "add_time"]
    list_editable = ["lesson", "name", "learn_times", "url"]


class CourseResourceAdmin(object):
    list_display = ["id", "course", "name", "file", "add_time"]
    search_fields = ["course", "name", "file"]
    list_filter = ["course", "name", "file", "add_time"]
    list_editable = ["course", "name", "file"]


xadmin.site.register(Courses, CoursesAdmin)
xadmin.site.register(Lessons, LessonsAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)
