import xadmin

from operations.models import UserAsk, UserCourse, UserFavorite, UserMsg, CourseComments, Banner


class UserAskAdmin(object):
    list_display = ["id", "name", "mobile", "course_name", "add_time"]
    search_fields = ["name", "mobile", "course_name"]
    list_filter = ["name", "mobile", "course_name", "add_time"]


class UserCourseAdmin(object):
    list_display = ["id", "user", "course", "add_time"]
    search_fields = ["user", "course"]
    list_filter = ["user", "course", "add_time"]


class UserFavoriteAdmin(object):
    list_display = ["id", "user", "fav_id", "fav_type", "add_time"]
    search_fields = ["user", "fav_id", "fav_type"]
    list_filter = ["user", "fav_id", "fav_type", "add_time"]


class UserMsgAdmin(object):
    list_display = ["id", "user", "message", "has_read", "add_time"]
    search_fields = ["user", "message", "has_read"]
    list_filter = ["user", "message", "has_read", "add_time"]


class CourseCommentsAdmin(object):
    list_display = ["id", "user", "course", "comments", "add_time"]
    search_fields = ["user", "course", "comments"]
    list_filter = ["user", "course", "comments", "add_time"]


class BannerAdmin(object):

    list_display = ["title", "image", "url", "index"]
    search_fields = ["title", "image", "url", "index"]
    list_filter = ["title", "image", "url", "index", "add_time"]


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMsg, UserMsgAdmin)
xadmin.site.register(Banner, BannerAdmin)
