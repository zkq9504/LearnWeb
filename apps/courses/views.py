from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


from courses.models import Courses, CourseTag, Video
from operations.models import UserFavorite, UserCourse, CourseComments


class CourseListView(View):
    """课程列表视图"""
    def get(self, request, *args, **kwargs):
        all_courses = Courses.objects.order_by("-add_time")
        keywords = request.GET.get("keywords", "")
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(detail__icontains=keywords))
        hot_courses = all_courses.order_by("-fav_nums")[:3]
        sort = request.GET.get("sort")
        # 对课程列表排序
        if sort == "hot":
            all_courses = all_courses.order_by("-fav_nums")
        elif sort == "students":
            all_courses = all_courses.order_by("-students")
        # 对课程列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=9, request=request)
        courses = p.page(page)
        return render(request, "course-list.html", {
            "all_courses": courses,
            "hot_courses": hot_courses,
            "sort": sort,
            "keywords": keywords,
            "s_type": "course"
        })


class CourseDetailView(View):
    """课程详情视图"""
    def get(self, request, course_id, *args, **kwargs):
        course = Courses.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=1, fav_id=course.id):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course.course_org.id):
                has_fav_org = True

        # 相关课程推荐
        tags = course.coursetag_set.all()
        tag_list = [tag.tag for tag in tags]
        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id)
        related_courses = set()
        for course_tag in course_tags:
            related_courses.add(course_tag.course)
        related_courses = list(related_courses)[:3]
        return render(request, "course-detail.html", {
            "course": course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
            "related_courses": related_courses,
        })


class CourseLessonView(LoginRequiredMixin, View):
    """课程章节视图"""
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        course = Courses.objects.get(id=course_id)
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()
        # 学过该课程的同学还学过的课程
        user_courses = UserCourse.objects.filter(course=course)
        users_id = [course_user.user.id for course_user in user_courses]
        related_courses = UserCourse.objects.filter(user_id__in=users_id).order_by("-course__students").exclude(course_id=course.id)[:5]

        return render(request, "course-lessons.html", {
            "course": course,
            "related_courses": related_courses,
        })


class CommentLessonView(LoginRequiredMixin, View):
    """课程评论视图"""
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        course = Courses.objects.get(id=course_id)
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            course.save()
            course.students += 1
            user_course.save()
        comments = CourseComments.objects.filter(course=course)
        # 学过该课程的同学还学过的课程
        user_courses = UserCourse.objects.filter(course=course)
        users_id = [course_user.user.id for course_user in user_courses]
        related_courses = UserCourse.objects.filter(user_id__in=users_id).order_by("-course__students").exclude(
            course_id=course.id)[:5]

        return render(request, "course-comment.html", {
            "course": course,
            "related_courses": related_courses,
            "comments": comments,
        })


class CourseVideoView(View):
    """课程视频视图"""
    login_url = "/login/"

    def get(self, request, course_id, video_id, *args, **kwargs):
        course = Courses.objects.get(id=course_id)
        video = Video.objects.get(id=video_id)
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            course.save()

            course.students += 1
            user_course.save()
        # 学过该课程的同学还学过的课程
        user_courses = UserCourse.objects.filter(course=course)
        users_id = [course_user.user.id for course_user in user_courses]
        related_courses = UserCourse.objects.filter(user_id__in=users_id).order_by("-course__students").exclude(
            course_id=course.id)[:5]

        return render(request, "course-play.html", {
            "course": course,
            "related_courses": related_courses,
            "video": video,
        })