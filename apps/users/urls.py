from django.urls import path
from django.conf.urls import url

from apps.users.views import UserInfoView, ImageUploadView, UpdatePwdView, UpdateMobileView
from apps.users.views import MyCourseView, MyFavoriteView, MyMessageView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='info'),
    url(r'^image/upload/$', ImageUploadView.as_view(), name='image'),
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    url(r'^update/mobile/$', UpdateMobileView.as_view(), name='update_mobile'),
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    url(r'^myfavorite/$', MyFavoriteView.as_view(), name='myfavorite'),
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),
]