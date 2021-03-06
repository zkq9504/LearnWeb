from django.urls import path
from django.conf.urls import url

from apps.organizations.views import OrgView, AddAskView, OrgHomeView, OrgTeacherView, OrgCourseView, OrgDescView
from apps.organizations.views import TeachersView, TeacherDetailView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name='list'),
    url(r'^add_ask/$', AddAskView.as_view(), name='add_ask'),
    # url(r'(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='home'),
    path('<int:org_id>/', OrgHomeView.as_view(), name='home'),
    path('<int:org_id>/course/', OrgCourseView.as_view(), name='course'),
    path('<int:org_id>/desc/', OrgDescView.as_view(), name='desc'),
    path('<int:org_id>/teacher/', OrgTeacherView.as_view(), name='teacher'),

    # 讲师列表
    url(r'^teachers/$', TeachersView.as_view(), name='teachers'),
    path('teachers/<int:teacher_id>/', TeacherDetailView.as_view(), name='teacher_detail'),
]